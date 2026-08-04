"""
Ejemplo de uso de punta a punta de fec_algebra.

Se corre directamente con:
    python3 examples/quickstart.py
(desde la raíz del proyecto, para que encuentre el paquete).
"""

import sys
import os

# agrega la raíz del proyecto al PYTHONPATH para poder correr esto sin instalar el paquete
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fec_algebra import GF, GFPoly


def main():
    print("=== Campo de Galois GF(2^8), primitivo del AES (0x1B) ===")
    field = GF(m=8, primitive_poly=0x1B)

    a = field(0x53)
    b = field(0xCA)
    print(f"a = {a!r}")
    print(f"b = {b!r}")

    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}   (0x53 * 0xCA = 0x01 -> a y b son inversos)")
    print(f"a.inverse() = {a.inverse()}")
    print(f"a / b = {a / b}")
    print(f"a ** 5 = {a ** 5}")

    print("\n=== Polinomios sobre GF(2^8) ===")
    p1 = GFPoly(field, [a, b, field(1)])   # a*x^2 + b*x + 1
    p2 = GFPoly(field, [field(1), field(0)])  # x
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p1 + p2 = {p1 + p2}")
    print(f"p1 * p2 = {p1 * p2}")

    cociente, resto = divmod(p1 * p2, p2)
    print(f"(p1*p2) // p2 = {cociente}  (debe ser p1)")
    print(f"(p1*p2) %  p2 = {resto}  (debe ser el polinomio nulo)")

    print(f"p1.scale(field(3)) = {p1.scale(field(3))}")
    print(f"p1.evaluate(field(7)) = {p1.evaluate(field(7))}")
    print(f"p1(field(7)) = {p1(field(7))}  (evaluate y __call__ son equivalentes)")

    p3 = GFPoly.from_roots(field, [a, b])
    print(f"\np3 = from_roots([a, b]) = {p3}")
    print(f"p3(a) = {p3(a)}  (debe ser 0)")
    print(f"p3(b) = {p3(b)}  (debe ser 0)")


if __name__ == "__main__":
    main()
