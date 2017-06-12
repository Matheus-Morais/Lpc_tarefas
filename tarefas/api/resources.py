from django.utils.baseconv import base64
from tastypie.resources import ModelResource
from tastypie import fields, utils
from tarefas.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.authentication import * #BasicAuthentication, ApiKeyAuthentication, get_username_field
from django.contrib.auth.models import User
from django.http.request import *

class UsuarioResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class ProjetoResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    class Meta:
        queryset = Projeto.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class TarefaResource(ModelResource):
    def obj_update(self, bundle, **kwargs):
        t = Tarefa.objects.get(pk=int(kwargs['pk']))
        u = bundle.data['usuario'].split('/')
        p = bundle.data['projeto'].split('/')

        usuario = User.objects.get(pk=int(u[4]))
        projeto = Projeto.objects.get(pk=int(p[4]))
        userLogado = bundle.request.user

        if t.usuario == userLogado:
            tarefa = Tarefa.objects.get(pk=int(kwargs['pk']))
            tarefa.nome = bundle.data['nome']
            tarefa.dataHora = bundle.data['dataHora']
            tarefa.usuario = usuario
            tarefa.projeto = projeto

            tarefa.save()
            bundle.obj = tarefa

            return bundle
        else:
            raise Unauthorized("Você não tem autorização para atualizar esse usuario!")

    def obj_delete(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk = int(kwargs['pk']))
        userLogado = bundle.request.user

        if tarefa.usuario == userLogado:
            tarefa.delete()
        else:
            raise Unauthorized("Você não tem autorização para deletar esse usuario!")

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split('/')
        p = bundle.data['projeto'].split('/')

        if not(Tarefa.objects.filter(nome=bundle.data['nome'])):
            ta = Tarefa()
            ta.nome = bundle.data['nome']
            ta.dataHora = bundle.data['dataHora']
            ta.usuario = User.objects.get(pk = u[4])
            ta.projeto = Projeto.objects.get(pk = p[4])

            ta.save()
            bundle.obj = ta
            return bundle
        else:
            raise Unauthorized("Não é permitido que uma tarefa seja associada a mais de um projeto!")

    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')
    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        #authorization = Authorization()
        authentication = ApiKeyAuthentication()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class ProjetoUsuarioResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')
    class Meta:
        queryset = ProjetoUsuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }
