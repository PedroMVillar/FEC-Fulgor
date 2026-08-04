"""
Tests de GF y GFElement: creación de elementos, suma, producto, inverso,
división y potencia sobre GF(2^m).

Para GF(2^8) los valores de referencia salen de tablas públicas de
multiplicación del campo de Rijndael (AES), para chequear la
implementación contra algo conocido y no solo contra sus propias cuentas.
"""

import pytest
from fec_algebra import GF, GFValueError, GFZeroDivisionError, GFFieldMismatchError


class TestConstruccionDelCampo:
    def test_orden_del_campo(self, gf256):
        """GF(2^8) tiene que tener 256 elementos."""
        assert gf256.order == 256

    def test_m_invalido_lanza_excepcion(self):
        """m tiene que ser un entero positivo."""
        with pytest.raises(GFValueError):
            GF(m=0, primitive_poly=0x1B)
        with pytest.raises(GFValueError):
            GF(m=-3, primitive_poly=0x1B)

    def test_primitivo_fuera_de_rango_lanza_excepcion(self):
        """primitive_poly tiene que entrar en m bits (sin el término x^m)."""
        with pytest.raises(GFValueError):
            GF(m=8, primitive_poly=0x1FF)  # se pasa de 8 bits


class TestCreacionDeElementos:
    def test_field_call_crea_elemento_valido(self, gf256):
        a = gf256(0x53)
        assert int(a) == 0x53
        assert a.field is gf256

    def test_valor_fuera_de_rango_lanza_excepcion(self, gf256):
        with pytest.raises(GFValueError):
            gf256(256)  # fuera de [0, 255]
        with pytest.raises(GFValueError):
            gf256(-1)

    def test_hexa_decimal_y_binario_representan_lo_mismo(self, gf256):
        """Da lo mismo en qué base se escribió el número en el código."""
        assert gf256(0x53) == gf256(83) == gf256(0b01010011)


class TestSuma:
    def test_suma_es_xor(self, gf256):
        """En GF(2^m) sumar es hacer XOR bit a bit."""
        a = gf256(0x53)
        b = gf256(0xCA)
        assert int(a + b) == 0x53 ^ 0xCA

    def test_elemento_es_su_propio_inverso_aditivo(self, gf256):
        """a + a siempre tiene que dar 0."""
        a = gf256(0x7F)
        assert int(a + a) == 0

    def test_neutro_aditivo(self, gf256):
        """Sumar 0 no cambia el elemento."""
        a = gf256(0x42)
        assert (a + gf256(0)) == a


class TestProducto:
    def test_producto_valor_conocido_aes(self, gf256):
        """0x53 * 0xCA da 0x01 en GF(2^8) con el primitivo del AES: son
        inversos entre sí. Valor sacado de tablas públicas de Rijndael."""
        a = gf256(0x53)
        b = gf256(0xCA)
        assert int(a * b) == 0x01

    def test_producto_por_cero(self, gf256):
        a = gf256(0x42)
        assert int(a * gf256(0)) == 0

    def test_producto_por_uno_es_neutro(self, gf256):
        a = gf256(0x42)
        assert (a * gf256(1)) == a

    def test_conmutatividad(self, gf256):
        a, b = gf256(0x53), gf256(0xCA)
        assert (a * b) == (b * a)

    def test_distributividad_respecto_a_la_suma(self, gf256):
        """a * (b + c) tiene que dar (a*b) + (a*c), propiedad de cuerpo."""
        a, b, c = gf256(0x53), gf256(0xCA), gf256(0x11)
        assert (a * (b + c)) == (a * b) + (a * c)


class TestInverso:
    def test_producto_por_inverso_es_uno(self, gf256):
        """a * a^-1 tiene que dar 1 para todo a != 0."""
        a = gf256(0x53)
        assert (a * a.inverse()) == gf256(1)

    def test_inverso_de_cero_lanza_excepcion(self, gf256):
        """El 0 no tiene inverso multiplicativo."""
        with pytest.raises(GFZeroDivisionError):
            gf256(0).inverse()

    def test_invert_operador_equivale_a_inverse(self, gf256):
        """~a tiene que dar lo mismo que a.inverse()."""
        a = gf256(0x53)
        assert (~a) == a.inverse()

    def test_inverso_de_uno_es_uno(self, gf256):
        assert gf256(1).inverse() == gf256(1)


class TestDivision:
    def test_division_por_si_mismo_es_uno(self, gf256):
        a = gf256(0x53)
        assert (a / a) == gf256(1)

    def test_division_por_cero_lanza_excepcion(self, gf256):
        with pytest.raises(GFZeroDivisionError):
            gf256(0x53) / gf256(0)

    def test_division_equivale_a_multiplicar_por_inverso(self, gf256):
        a, b = gf256(0x53), gf256(0xCA)
        assert (a / b) == (a * b.inverse())


class TestPotencia:
    def test_potencia_cero_es_uno(self, gf256):
        """Por convención a^0 == 1 para todo a, incluso a == 0."""
        a = gf256(0x53)
        assert int(a ** 0) == 1

    def test_potencia_uno_es_identidad(self, gf256):
        a = gf256(0x53)
        assert (a ** 1) == a

    def test_potencia_coincide_con_multiplicaciones_sucesivas(self, gf256):
        """Compara square-and-multiply contra el cálculo directo."""
        a = gf256(0x53)
        esperado = gf256(1)
        for _ in range(5):
            esperado = esperado * a
        assert (a ** 5) == esperado

    def test_potencia_orden_menos_uno_es_uno(self, gf256):
        """Es la consecuencia de Fermat en cuerpos finitos: a^(orden - 1) == 1 para todo a != 0."""
        a = gf256(0x53)
        assert (a ** (gf256.order - 1)) == gf256(1)


class TestCamposDistintos:
    def test_operar_entre_campos_distintos_lanza_excepcion(self, gf256, gf16):
        """No se puede sumar un elemento de GF(2^8) con uno de GF(2^4)."""
        a = gf256(0x53)
        b = gf16(0x5)
        with pytest.raises(GFFieldMismatchError):
            a + b

    def test_multiplicar_entre_campos_distintos_lanza_excepcion(self, gf256, gf16):
        with pytest.raises(GFFieldMismatchError):
            gf256(0x53) * gf16(0x5)
