import pytest

from app.utils.forms import formatar_texto, somente_numeros, validar_cpf


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("  coca   cola  ", "Coca Cola"),
        ("ARROZ TIPO 1", "Arroz Tipo 1"),
        ("   ", ""),
        ("", ""),
        (None, None),
    ],
)
def test_formatar_texto(entrada, esperado):
    assert formatar_texto(entrada) == esperado


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("123.456.789-00", "12345678900"),
        ("(11) 98765-4321", "11987654321"),
        ("abc123def45", "12345"),
        ("", ""),
        (None, None),
    ],
)
def test_somente_numeros(entrada, esperado):
    assert somente_numeros(entrada) == esperado


@pytest.mark.parametrize(
    "cpf",
    [
        "52998224725",
        "529.982.247-25",
        "11144477735",
    ],
)
def test_validar_cpf_validos(cpf):
    assert validar_cpf(cpf) is True


@pytest.mark.parametrize(
    "cpf",
    [
        "00000000000",
        "11111111111",
        "111.111.111-11",
        "52998224724",  # dígito verificador inválido
        "1234567890",   # menos de 11 dígitos
        "123456789012", # mais de 11 dígitos
        "abcdefghijk",
        "",
        None,
    ],
)
def test_validar_cpf_invalidos(cpf):
    assert validar_cpf(cpf) is False
