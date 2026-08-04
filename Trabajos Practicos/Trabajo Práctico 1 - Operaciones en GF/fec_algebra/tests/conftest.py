"""
Fixtures compartidas para los tests de fec_algebra.

Como campo de referencia se usa GF(2^8) con el polinomio primitivo del
AES/Rijndael: x^8 + x^4 + x^3 + x + 1 (0x11B, o 0x1B sin el bit x^8
implícito). Sirve porque sus valores están documentados y verificados en
tablas públicas de Rijndael, así se puede chequear la implementación
contra algo externo y no solo contra sí misma.

También hay un GF(2^4) con primitivo x^4 + x + 1 (0x3), un campo chico
que sirve para verificar cuentas a mano y para los tests de GFPoly, donde
conviene tener pocos elementos.
"""

import pytest
from fec_algebra import GF


@pytest.fixture
def gf256():
    """GF(2^8) con el polinomio primitivo estándar del AES (0x1B)."""
    return GF(m=8, primitive_poly=0x1B)


@pytest.fixture
def gf16():
    """GF(2^4) con polinomio primitivo x^4 + x + 1 (0x3)."""
    return GF(m=4, primitive_poly=0x3)
