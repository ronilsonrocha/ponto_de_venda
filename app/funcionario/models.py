from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from app.utils.forms import somente_numeros, validar_cpf

class Funcionario(models.Model):

    class Cargo(models.TextChoices):
        GERENTE = 'GERENTE', 'Gerente'
        CAIXA = 'CAIXA', 'Operador de Caixa'

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='funcionario',
        verbose_name="Usuário",
    )
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    cargo = models.CharField("Cargo", max_length=20, choices=Cargo.choices, default=Cargo.CAIXA)
    data_admissao = models.DateField("Data de Admissão", blank=True, null=True)
    ativo = models.BooleanField("Funcionário Ativo", default=True)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Data de Atualização", auto_now=True)

    # Executa validação/normalização completa antes de gravar no banco
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # Padroniza CPF/telefone (apenas dígitos) e valida as regras antes de salvar
    def clean(self):
        errors = {}

        if self.cpf:
            self.cpf = somente_numeros(self.cpf)
            if not validar_cpf(self.cpf):
                errors['cpf'] = 'CPF inválido.'

        if self.telefone:
            telefone_limpo = somente_numeros(self.telefone)
            if not telefone_limpo:
                self.telefone = None
            elif len(telefone_limpo) not in (10, 11):
                errors['telefone'] = 'O telefone deve ter 10 ou 11 dígitos (com DDD).'
            else:
                self.telefone = telefone_limpo

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

    class Meta:
        ordering = ['usuario__first_name', 'usuario__username']
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'