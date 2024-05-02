from rest_framework import viewsets
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import UserLog

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer





@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='Logged in')

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserLog.objects.create(user=user, action='Logged out')

@receiver(m2m_changed, sender=User.roles.through)
def user_role_changed_handler(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        UserLog.objects.create(user=instance.user, action=f'Role {action}')
