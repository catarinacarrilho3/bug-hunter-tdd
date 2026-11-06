import pytest

from Calculadora import fatorial, multiplicacao, raiz_quadrada, subtracao


# BUG-004: fatorial retornava sempre 0
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


# BUG-005: ainda não corrigido, o teste documenta o comportamento esperado
@pytest.mark.xfail(reason="BUG-005: fatorial de negativo ainda retorna 1")
def test_fatorial_negativo_levanta_erro():
    with pytest.raises(ValueError):
        fatorial(-3)


# Testes de regressão: funções não alteradas pela correção
def test_subtracao():
    assert subtracao(5, 3) == 2


def test_multiplicacao():
    assert multiplicacao(4, 3) == 12


def test_raiz_quadrada_positiva():
    assert raiz_quadrada(9) == 3


def test_raiz_quadrada_negativa_retorna_erro():
    assert raiz_quadrada(-4).startswith("Erro")
