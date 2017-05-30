from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField('nome', max_length=200)
    email = models.CharField('email', max_length=200)
    senha = models.CharField('senha', max_length=20)

class Projeto(models.Model):
    nome = models.CharField('nome', max_length=200)

class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=200)
    dataHora = models.DateTimeField('dataHora', default=timezone.now)
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')

class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')
