__author__ = 'milkyway'
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.db import models
from django.contrib.auth.models import User
from info.models import UserProfile,Interest, Interest_Tag
from tastypie.models import create_api_key
from tastypie import fields

models.signals.post_save.connect(create_api_key, sender=User)
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        excludes=['email','password','is_active','is_staff','is_superuser','id']
        authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'username': ALL,
            }

class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = UserProfile.objects.all()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

class InterestResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')

    class Meta:
        queryset = Interest.objects.all()
        allowed_methods = ['get','post','put']
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

class InterestTagResource(ModelResource):
    interest = fields.ManyToManyField(InterestResource,'interests')
    class Meta:
        queryset = Interest_Tag.objects.all()
        authorization = Authorization()
        filtering = {
            'interests': ALL_WITH_RELATIONS
        }