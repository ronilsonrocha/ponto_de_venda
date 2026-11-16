def formatar_texto(texto):
    if texto:
        return " ".join(texto.split()).title()
    return texto

def somente_numeros(texto):
    """Remove qualquer caractere que não seja dígito."""
    if texto:
        return "".join(char for char in str(texto) if char.isdigit())
    return texto

def validar_cpf(cpf):
    """
    Valida um CPF (11 dígitos e dígitos verificadores).
    Obs: cpf chutados não irão funcionar
    """
    numeros = somente_numeros(cpf) or ""
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    # Fórmula matemática para calcular os 2 dígitos verificadores do CPF
    for i in (9, 10):
        soma = 0
        peso = i + 1
        for j in range(i):
            soma += int(numeros[j]) * peso
            peso -= 1
        digito = ((soma * 10) % 11) % 10
        if digito != int(numeros[i]):
            return False
    return True