import pytest

from Calculadora import fatorial


@pytest.mark.parametrize(
    "n, esperado",
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (5, 120),
        (10, 3628800),
    ],
)
def test_fatorial_valores_conhecidos(n, esperado):
    assert fatorial(n) == esperado
