from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

'''class Usuario(models.Model):
    usuario = models.OneToOneField(User, default='')'''''

class Projeto(models.Model):
    nome = models.CharField('nome', max_length=200)

class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=200)
    dataHora = models.DateTimeField('dataHora', default=timezone.now)
    usuario = models.ForeignKey(User, default='')
    projeto = models.ForeignKey('Projeto')

class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey(User, default='')
    projeto = models.ForeignKey('Projeto')
