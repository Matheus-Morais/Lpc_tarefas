from tastypie.resources import ModelResource
from tastypie import fields, utils
from tarefas.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class UsuarioResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith')
        }

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']

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
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel deletar toda a lista!")

    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split('/')
        p = bundle.data['projeto'].split('/')

        if not(Tarefa.objects.filter(nome=bundle.data['nome'])):
            ta = Tarefa()
            ta.nome = bundle.data['nome']
            ta.dataHora = bundle.data['dataHora']
            ta.usuario = Usuario.objects.get(pk = u[4])
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
        authorization = Authorization()
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
