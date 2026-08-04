# fec_algebra

Librería chica en Python para trabajar con campos de Galois `GF(2^m)` y
polinomios con coeficientes en esos campos. Es el Trabajo Práctico 1 del
curso de FEC (Fundación Fulgor, 2026).

## Instalación

No hace falta instalar nada como paquete: alcanza con tener la carpeta
`fec_algebra/` en el `PYTHONPATH`, o correr los scripts desde la raíz
del repositorio.

Para los tests hace falta `pytest`:

```bash
pip install pytest
pytest tests/ -v
```

## Estructura

```
fec_algebra/
├── fec_algebra/
│   ├── __init__.py       # API pública
│   ├── exceptions.py     # excepciones propias
│   ├── gf.py             # clase GF: campo de Galois GF(2^m)
│   ├── gf_element.py     # clase GFElement: elemento del campo
│   └── gf_poly.py        # clase GFPoly: polinomios sobre GF(2^m)
├── tests/                 # tests con pytest
├── examples/
│   └── quickstart.py      # ejemplo de uso de punta a punta
└── README.md
```

## Conceptos clave

- `GF(m, primitive_poly)`: el campo `GF(2^m)`. `primitive_poly` es el
  polinomio primitivo `P(x)` que define la reducción, como entero de `m`
  bits (sin el término `x^m`, que queda implícito).
- `GFElement`: un elemento del campo. No se instancia directo, se crea
  llamando al campo como si fuera una función, `field(valor)`. Cada
  elemento es un entero en `[0, 2^m - 1]` que representa un polinomio
  binario de grado `< m` (los bits son los coeficientes).
- `GFPoly`: un polinomio cuyos coeficientes son elementos de un `GF`.

## Teoría de fundamentación

Esto sigue básicamente lo que da Lin & Costello, *Error Control Coding*
(2da ed.), cap. 2, que es donde el curso apoya toda la construcción de
`GF(2^m)`.

`GF(2^m)` es un campo finito de `2^m` elementos, armado como polinomios
módulo un polinomio irreducible (y primitivo, para que exista un
generador de todo el grupo multiplicativo) de grado `m` sobre `GF(2)`.
Es justo lo que hace `GF.multiply`: reduce el producto de dos polinomios
módulo `primitive_poly`.

Un elemento primitivo `α` es un generador del grupo multiplicativo de
`GF(2^m)`: `α^0, α^1, ..., α^(2^m−2)` recorren los `2^m−1` elementos no
nulos, y el polinomio primitivo es el de grado mínimo del que `α` es
raíz. No alcanza con que `primitive_poly` sea irreducible nada más, el
libro marca que un irreducible que no es primitivo hace que `α` no
genere todos los elementos no nulos, y ahí se rompe (sin aviso)
cualquier cosa armada sobre tabla de logaritmos. La librería no
verifica primitividad, asume que el `primitive_poly` que recibe ya lo
es, igual que lo da el enunciado del TP como dato.

Hay dos formas de representar un elemento: la vectorial (los `m`
bits/coeficientes, que es la que usa `GFElement` internamente, cómoda
para sumar por XOR) y la exponencial (como potencia de `α`, cómoda para
multiplicar y dividir sumando y restando exponentes). `GFElement` guarda
siempre la forma vectorial; la exponencial se reconstruye fácil armando
una tabla de logaritmo discreto sobre las potencias de `α` (así se hace
en el notebook `TP2_Guia_Ejercicios.ipynb` para escribir coeficientes
como `α^i`).

En `GF(2^m)` sumar es hacer XOR y restar es lo mismo que sumar (en
característica 2, `−1 = 1`). Por eso `GFElement` no tiene `__sub__`, ver
más abajo.

El orden de un elemento es el menor entero positivo `e` tal que
`α^e = 1`, y siempre divide a `2^m − 1`. `GF.inverse` usa justo esta
propiedad: para todo `a ≠ 0`, `a^(2^m−1) = 1` (es la versión de Fermat
para cuerpos finitos), de donde `a^(2^m−2)` es el inverso de `a`.

Para los ejercicios de códigos lineales del notebook (matriz generadora
`G`, matriz de verificación `H`, forma sistemática, síndrome), la
referencia es el cap. 3 del mismo libro, "Linear Block Codes"; el
detalle de cada cita está en el notebook.

## Ejemplo rápido

```python
from fec_algebra import GF, GFPoly

# GF(2^8) con el polinomio primitivo del AES: x^8+x^4+x^3+x+1
field = GF(m=8, primitive_poly=0x1B)

a = field(0x53)
b = field(0xCA)

a + b          # suma (XOR)
a * b          # producto módulo el primitivo -> da 0x01 (son inversos)
a.inverse()    # inverso multiplicativo (equivale a ~a)
a / b          # división
a ** 5         # potencia (square-and-multiply)

# Polinomios sobre GF(2^8)
p1 = GFPoly(field, [a, b, field(1)])   # a*x^2 + b*x + 1
p2 = GFPoly(field, [field(1), field(0)])  # x

p1 + p2
p1 * p2
cociente, resto = divmod(p1, p2)   # o p1 // p2  /  p1 % p2
p1.scale(field(3))
p1.evaluate(field(7))               # o directamente p1(field(7))
GFPoly.from_roots(field, [a, b])    # (x - a)(x - b)
```

## Algunas decisiones al armar esto

- Los elementos se representan como objetos (`GFElement`) y no como
  enteros a secas: permite escribir `a + b`, `a * b`, `a ** n`, etc. con
  la sintaxis normal de Python (sobrecarga de operadores), y de paso
  evita mezclar por error elementos de campos distintos, porque se
  valida y tira `GFFieldMismatchError`.
- No hay `__sub__`. En `GF(2^m)` restar es lo mismo que sumar, así que
  no tiene sentido tener una operación aparte que sugiera algo distinto.
- Dividir por 0 o invertir el 0 tira `GFZeroDivisionError` explícita, en
  vez de devolver `None` o algo silencioso.
- La potencia está hecha con square-and-multiply (`GF.power`), en
  `O(log n)` multiplicaciones en vez de `O(n)`.
- `GFPoly` mantiene el invariante de no tener ceros a la izquierda
  (salvo el polinomio nulo, que se representa como `[0]`). Se normaliza
  en un único lugar (`_strip_leading_zeros`), en el constructor, así que
  cualquier operación que devuelve un `GFPoly` nuevo ya sale normalizada.
- El grado del polinomio nulo es `-1`, como se usa siempre en álgebra.

## Excepciones

| Excepción | Cuándo salta |
|---|---|
| `GFValueError` | Valor fuera de rango, `m` inválido, coeficiente inválido |
| `GFZeroDivisionError` | Inverso o división por el elemento/polinomio 0 |
| `GFFieldMismatchError` | Operar entre elementos/polinomios de campos distintos |

Todas heredan de `GFError`, para poder capturar cualquier error del
paquete con un solo `except` si se quiere.
