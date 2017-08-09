# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_dataImg(value):
	if not (value.name.endswith('.jpg') or value.name.endswith('.png')):
		raise ValidationError(u'not supported file')


# Create your models here.
class Image(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=512)
	img = models.FileField(validators=[validate_dataImg])
	likes = models.IntegerField(default=0)
	uploaded = models.DateTimeField(auto_now_add = True, null=True)

	def __str__(self):
		return str(self.user.username) + '-' + str(self.id)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	liked = models.DateTimeField(auto_now_add = True, null=True)

	def __str__(self):
		return str(self.user.username) + '-' + str(self.image.id)

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	cmnt = models.CharField(max_length=512)
	commented = models.DateTimeField(auto_now_add = True, null=True)

	def __str__(self):
		return str(self.user.username) + '-' + str(self.image.id)
		
		