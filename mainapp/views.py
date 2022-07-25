from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from mainapp.models import User, Quota, Resources
from mainapp.serializers import UserModelSerializer, QuotaModelSerializer, ResourcesModelSerializer


class AuthView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, requset):
        email = requset.POST.get('email')
        password = requset.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            context = {
                'token': str(token[0].key)
            }
            return Response(context)
        context = {
            'error': {'msg': 'email or password is incorrect'}
        }
        return Response(context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get_permissions(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied({'permission denied': 'You do not have permission on this url'})
        return super(UserViewSet, self).get_permissions()


class QuotaViewSet(viewsets.ModelViewSet):
    queryset = Quota.objects.all()
    serializer_class = QuotaModelSerializer

    def get_permissions(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied({'permission denied': 'You do not have permission on this url'})
        return super(QuotaViewSet, self).get_permissions()


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resources.objects.all()
    serializer_class = ResourcesModelSerializer

    def get_serializer_context(self):
        context = super(ResourceViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(user=self.request.user)
        return super(ResourceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            object_id = self.kwargs['pk']
            users_resources = self.queryset.filter(user=self.request.user).values('id')
            resources_ids = []
            for ids in users_resources:
                resources_ids.append(ids['id'])
            if int(object_id) not in resources_ids:
                raise PermissionDenied({'permission denied': 'This is not your resource'})
        return super(ResourceViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            object_id = self.kwargs['pk']
            users_resources = self.queryset.filter(user=self.request.user).values('id')
            resources_ids = []
            for ids in users_resources:
                resources_ids.append(ids['id'])
            if int(object_id) not in resources_ids:
                raise PermissionDenied({'permission denied': 'This is not your resource'})
        return super(ResourceViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            object_id = self.kwargs['pk']
            users_resources = self.queryset.filter(user=self.request.user).values('id')
            resources_ids = []
            for ids in users_resources:
                resources_ids.append(ids['id'])
            if int(object_id) not in resources_ids:
                raise PermissionDenied({'permission denied': 'This is not your resource'})
        return super(ResourceViewSet, self).retrieve(request, *args, **kwargs)



