# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .validation import Validation
import bcrypt

class UserManager(models.Manager):

    def check_login(self, post_data):
        # create object that will be returned
        input_reqs = [
            ('email', 'email', post_data['email']),
            ('pass_check', 'password', post_data['password'], post_data['password'], 8, 16)
        ]
        validated = Validation(input_reqs)
        # Try to get user object with email address
        try:
            user = User.objects.get(email=validated.data['email'])
        except:
            user = False
            validated.errors.append('User Does not exist')
            return validated
        if user:
            validated.data['id'] = user.id
            validated.data['hash'] = user.password.encode()
            if bcrypt.hashpw(post_data['password'].encode(), validated.data['hash']) == validated.data['hash']:
                validated.data['status'] = 'Authenticated'
            else:
                validated.data['status'] = 'Failed'
        return validated

    def check_register(self, post_data):
        input_reqs = [
            ('alpha', 'f_name', post_data['f_name']),
            ('alpha', 'l_name', post_data['l_name']),
            ('email', 'email', post_data['email']),
            ('pass_check', 'password', post_data['password'], post_data['confirm_password'], 8, 16)
        ]
        validated = Validation(input_reqs)
        return validated

# Create your models here.
class User(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=40)
    email = models.CharField(max_length=65)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class SecretManager(models.Manager):
    def create_secret(self, post_data):
        user_id = post_data['user_id']
        secret = post_data['secret']
        data = {
            'errors': [],
            'secret_id': None
        }
        if len(secret) > 0 and len(secret) < 1000:
            try:
                user = User.objects.get(id=user_id)
            except:
                user = False
                data['errors'].append('There was a problem with your user id. Contact Site Administrator')
            if user:
                try:
                    new_secret = Secret.objects.create(user = user, secret = secret)
                except:
                    new_secret = False
                    data['errors'].append('There was an issue with creating your secret. Contact Site Administrator')
        else:
            data['errors'].append('The length of your Secret is outside of the restrictions provided')
        if len(data['errors']) > 0:
            return data
        else:
            data['secret_id'] = new_secret.id
            return data

class Secret(models.Model):
    secret = models.TextField(max_length=1000)
    user = models.ForeignKey(User)
    user_likes = models.ManyToManyField(User,related_name='liked_secrets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SecretManager()
