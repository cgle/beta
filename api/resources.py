__author__ = 'milkyway'
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from django.db import models
from django.contrib.auth.models import User
from info.models import UserProfile,Interest, Interest_Tag, KoinboxUser, Friends
from tastypie.models import create_api_key
from tastypie import fields

models.signals.post_save.connect(create_api_key, sender=User)
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        excludes=['email','is_active','is_staff','is_superuser','id']
        authorization = Authorization()
        filtering = {
            'username': ALL,
            }

class MyKoinboxResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = KoinboxUser.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'username': ALL,
            }

class FriendResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = Friends.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'username': ALL,
            }

class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = UserProfile.objects.all()
        allowed_methods = ['get']
        authentication  = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }
    def obj_create(self, bundle, request=None, **kwargs):
        return super(EnvironmentResource, self).obj_create(bundle, request, user=request.user)
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class OtherUserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = UserProfile.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }


class CreateUserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = UserProfile.objects.all()
        allowed_methods = ['post','put']
        resource_name = 'createprofile'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

class InterestResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')

    class Meta:
        queryset = Interest.objects.all()
        allowed_methods = ['get']
        authentication  = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }
    def obj_create(self, bundle, request=None, **kwargs):
        return super(EnvironmentResource, self).obj_create(bundle, request, user=request.user)
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

class CreateInterestResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')
    class Meta:
        queryset = Interest.objects.all()
        allowed_methods = ['get','post','put','delete']
        resource_name = 'createinterest'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

class OtherUserInterestResource(ModelResource):
    user = fields.ForeignKey(UserResource,'user')

    class Meta:
        queryset = Interest.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS
        }

class InterestTagResource(ModelResource):
    interest = fields.ManyToManyField(InterestResource,'interests')
    class Meta:
        queryset = Interest_Tag.objects.all()
        allowed_methods = ['get','post']
        authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'interests': ALL_WITH_RELATIONS
        }

class OtherUserInterestTagResource(ModelResource):
    interest = fields.ManyToManyField(InterestResource,'interests')

    class Meta:
        queryset = Interest_Tag.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {
            'interests': ALL_WITH_RELATIONS
        }

class UserSignUpResource(ModelResource):
    class Meta:
        object_class = User
        queryset = User.objects.all()
        allowed_methods = ['post']
        include_resource_uri = False
        resource_name = 'newuser'
        authorization = Authorization()
        models.signals.post_save.connect(create_api_key, sender=User)

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(UserSignUpResource, self).obj_create(bundle, request, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('The username already exists')
        return bundle