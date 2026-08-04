"""
Tests de GFPoly: construcción, suma, producto, división, escalado,
evaluación y construcción a partir de raíces, sobre polinomios con
coeficientes en GF(2^m).

Se usa sobre todo GF(2^4) (campo chico) para que los polinomios de
ejemplo sean fáciles de seguir a mano, y GF(2^8) para los casos que
tienen que ser coherentes con los tests de GFElement.
"""

import pytest
from fec_algebra import GFPoly, GFValueError, GFFieldMismatchError, GFZeroDivisionError


class TestConstruccion:
    def test_acepta_coeficientes_como_int(self, gf16):
        """El constructor tiene que convertir enteros a GFElement solo."""
        p = GFPoly(gf16, [1, 2, 3])
        assert int(p[0]) == 3 and int(p[1]) == 2 and int(p[2]) == 1

    def test_recorta_ceros_a_la_izquierda(self, gf16):
        """[0, 0, 3, 5] es el mismo polinomio que [3, 5]: los ceros
        iniciales no cuentan y no tendrían que quedar en la
        representación interna."""
        p1 = GFPoly(gf16, [0, 0, 3, 5])
        p2 = GFPoly(gf16, [3, 5])
        assert p1 == p2
        assert p1.degree == 1

    def test_polinomio_nulo_se_representa_como_un_solo_cero(self, gf16):
        p = GFPoly(gf16, [0, 0, 0])
        assert p.degree == -1
        assert p == GFPoly.zero(gf16)

    def test_coeficientes_vacios_lanza_excepcion(self, gf16):
        with pytest.raises(GFValueError):
            GFPoly(gf16, [])

    def test_coeficiente_de_otro_campo_lanza_excepcion(self, gf16, gf256):
        with pytest.raises(GFFieldMismatchError):
            GFPoly(gf16, [gf256(1), gf256(0)])


class TestGrado:
    def test_grado_polinomio_nulo_es_menos_uno(self, gf16):
        assert GFPoly.zero(gf16).degree == -1

    def test_grado_constante_es_cero(self, gf16):
        assert GFPoly(gf16, [5]).degree == 0

    def test_grado_coincide_con_cantidad_de_coeficientes_menos_uno(self, gf16):
        assert GFPoly(gf16, [1, 0, 3, 2]).degree == 3


class TestGetItem:
    def test_acceso_a_coeficientes_por_grado(self, gf16):
        # p(x) = 1*x^2 + 0*x + 3
        p = GFPoly(gf16, [1, 0, 3])
        assert int(p[0]) == 3   # término independiente
        assert int(p[1]) == 0
        assert int(p[2]) == 1

    def test_indice_mayor_al_grado_devuelve_cero(self, gf16):
        p = GFPoly(gf16, [1, 0, 3])
        assert int(p[10]) == 0


class TestSuma:
    def test_suma_de_polinomios_de_igual_grado(self, gf16):
        p1 = GFPoly(gf16, [1, 2, 3])
        p2 = GFPoly(gf16, [4, 5, 6])
        esperado = GFPoly(gf16, [gf16(1) + gf16(4), gf16(2) + gf16(5), gf16(3) + gf16(6)])
        assert (p1 + p2) == esperado

    def test_suma_de_polinomios_de_distinto_grado(self, gf16):
        """La suma tiene que alinear bien los términos de menor grado
        aunque los polinomios no tengan la misma cantidad de coeficientes."""
        p1 = GFPoly(gf16, [1, 0, 0])       # x^2
        p2 = GFPoly(gf16, [1])              # 1
        resultado = p1 + p2
        assert int(resultado[2]) == 1
        assert int(resultado[0]) == 1

    def test_sumar_un_polinomio_consigo_mismo_da_cero(self, gf16):
        """Como sumar en GF(2^m) es XOR, p + p == 0."""
        p = GFPoly(gf16, [1, 2, 3])
        assert (p + p) == GFPoly.zero(gf16)

    def test_suma_entre_campos_distintos_lanza_excepcion(self, gf16, gf256):
        p1 = GFPoly(gf16, [1, 2])
        p2 = GFPoly(gf256, [1, 2])
        with pytest.raises(GFFieldMismatchError):
            p1 + p2


class TestProducto:
    def test_producto_por_polinomio_nulo_es_nulo(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        assert (p * GFPoly.zero(gf16)) == GFPoly.zero(gf16)

    def test_grado_del_producto_es_suma_de_grados(self, gf16):
        p1 = GFPoly(gf16, [1, 0])   # grado 1
        p2 = GFPoly(gf16, [1, 1, 0])  # grado 2
        assert (p1 * p2).degree == 3

    def test_producto_coincide_con_evaluacion_punto_a_punto(self, gf16):
        """Si c = p1 * p2, entonces c(x) == p1(x) * p2(x) para cualquier
        x del campo (chequea que producto y evaluación sean coherentes)."""
        p1 = GFPoly(gf16, [1, 2, 3])
        p2 = GFPoly(gf16, [4, 5])
        producto = p1 * p2
        for v in range(gf16.order):
            x = gf16(v)
            assert producto(x) == p1(x) * p2(x)


class TestDivision:
    def test_division_exacta(self, gf16):
        """Multiplicando p1 * p2 y dividiendo por p2 se tiene que recuperar p1, con resto 0."""
        p1 = GFPoly(gf16, [1, 2, 3])
        p2 = GFPoly(gf16, [1, 1])
        producto = p1 * p2
        cociente, resto = divmod(producto, p2)
        assert cociente == p1
        assert resto == GFPoly.zero(gf16)

    def test_floordiv_y_mod_coinciden_con_divmod(self, gf16):
        p1 = GFPoly(gf16, [1, 0, 1, 1])
        p2 = GFPoly(gf16, [1, 1])
        cociente, resto = divmod(p1, p2)
        assert (p1 // p2) == cociente
        assert (p1 % p2) == resto

    def test_dividendo_de_grado_menor_da_cociente_nulo(self, gf16):
        p1 = GFPoly(gf16, [1])          # grado 0
        p2 = GFPoly(gf16, [1, 0, 1])    # grado 2
        cociente, resto = divmod(p1, p2)
        assert cociente == GFPoly.zero(gf16)
        assert resto == p1

    def test_dividir_por_nulo_lanza_excepcion(self, gf16):
        p1 = GFPoly(gf16, [1, 2, 3])
        with pytest.raises(GFZeroDivisionError):
            divmod(p1, GFPoly.zero(gf16))

    def test_relacion_fundamental_dividendo_igual_cociente_por_divisor_mas_resto(self, gf16):
        """Toda división polinómica tiene que cumplir: dividendo == cociente * divisor + resto."""
        p1 = GFPoly(gf16, [1, 0, 1, 1, 0])
        p2 = GFPoly(gf16, [1, 1, 1])
        cociente, resto = divmod(p1, p2)
        assert (cociente * p2 + resto) == p1


class TestEscalado:
    def test_escalado_por_uno_no_modifica(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        assert p.scale(gf16(1)) == p

    def test_escalado_por_cero_da_polinomio_nulo(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        assert p.scale(gf16(0)) == GFPoly.zero(gf16)

    def test_escalado_multiplica_cada_coeficiente(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        k = gf16(5)
        escalado = p.scale(k)
        for i in range(3):
            assert escalado[i] == p[i] * k


class TestEvaluacion:
    def test_evaluar_en_cero_da_termino_independiente(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        assert p.evaluate(gf16(0)) == gf16(3)

    def test_poly_call_es_alias_de_evaluate(self, gf16):
        p = GFPoly(gf16, [1, 2, 3])
        x = gf16(4)
        assert p(x) == p.evaluate(x)

    def test_polinomio_constante_evalua_siempre_igual(self, gf16):
        p = GFPoly(gf16, [7])
        for v in range(gf16.order):
            assert p(gf16(v)) == gf16(7)


class TestFromRoots:
    def test_raices_anulan_el_polinomio(self, gf16):
        """Si r es una raíz usada para construir el polinomio, evaluarlo en r tiene que dar 0."""
        r1, r2 = gf16(3), gf16(7)
        p = GFPoly.from_roots(gf16, [r1, r2])
        assert p(r1) == gf16(0)
        assert p(r2) == gf16(0)

    def test_grado_coincide_con_cantidad_de_raices(self, gf16):
        p = GFPoly.from_roots(gf16, [gf16(1), gf16(2), gf16(3)])
        assert p.degree == 3

    def test_conjunto_vacio_de_raices_da_polinomio_uno(self, gf16):
        """El producto vacío da 1, convención matemática de siempre."""
        p = GFPoly.from_roots(gf16, [])
        assert p == GFPoly(gf16, [1])

    def test_valor_no_raiz_no_anula_el_polinomio(self, gf16):
        """Chequeo extra: un elemento que no es raíz no debería anular el polinomio."""
        r1, r2 = gf16(3), gf16(7)
        p = GFPoly.from_roots(gf16, [r1, r2])
        no_raices = [gf16(v) for v in range(gf16.order) if v not in (3, 7)]
        assert any(p(x) != gf16(0) for x in no_raices)
