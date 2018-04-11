from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.encoding import python_2_unicode_compatible

from guardian.mixins import GuardianUserMixin
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField('title', max_length=64)

    def __str__(self):
        return self.title


class DynamicAccessor(object):

    def __init__(self):
        pass

    def __getattr__(self, key):
        return DynamicAccessor()


class ProjectUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)


class ProjectGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey('Project', on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.name


Project.not_a_relation_descriptor = DynamicAccessor()


class MixedGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey('Mixed', on_delete=models.CASCADE)


@python_2_unicode_compatible
class Mixed(models.Model):
    """
    Model for tests obj perms checks with generic user object permissions model
    and direct group object permissions model.
    """
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class ReverseMixedUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey('ReverseMixed', on_delete=models.CASCADE)


@python_2_unicode_compatible
class ReverseMixed(models.Model):
    """
    Model for tests obj perms checks with generic group object permissions model
    and generic group object permissions model.
    """
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class LogEntryWithGroup(LogEntry):
    group = models.ForeignKey('auth.Group', null=True, blank=True, on_delete=models.CASCADE)

    objects = models.Manager()


class NonIntPKModel(models.Model):
    """
    Model for testing whether get_objects_for_user will work when the objects to
    be returned have non-integer primary keys.
    """
    char_pk = models.CharField(primary_key=True, max_length=128)


class CustomUser(AbstractUser, GuardianUserMixin):
    custom_id = models.AutoField(primary_key=True)


class CustomUsernameUser(AbstractBaseUser, GuardianUserMixin):
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class CustomUuidUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class CustomUuidUser(AbstractBaseUser, GuardianUserMixin):
    custom_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    USERNAME_FIELD = 'username'
    objects = CustomUuidUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
