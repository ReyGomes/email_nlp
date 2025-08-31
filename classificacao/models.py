from django.db import models

# Create your models here.
class Email(models.Model):
    assunto = models.CharField(max_length=150)
    texto = models.CharField(max_length=1000)
    arquivo = models.FileField(upload_to='emails/', null=True, blank=True) 
    produtivo = models.BooleanField(default=False)
    resposta = models.TextField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)