from django.db import models

# Create your models here.
class Venda(models.Model):
    
    
    class Meta():
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'