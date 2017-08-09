# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Image, Comment, Like
from .forms import userRegForm, logForm, addImageForm, commentForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def home(request):
	context = {}
	context['images_latest'] = Image.objects.all().order_by('-uploaded')[:6]
	context['images_popular'] = Image.objects.all().order_by('-likes')[:6]
	context['all'] = True
	return render(request, 'home.html',context)

def logIn(request):
	form = logForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return redirect(home)
			else:
				return render(request,'login.html',{'form':form, 'err':"Invalid username or password"})

	return render(request, 'login.html', {'form':form})

def register(request):
	form = userRegForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			if form.cleaned_data['password'] == form.cleaned_data['password2']:
				user = form.save(commit=False)
				user.set_password(form.cleaned_data['password'])
				user.save()
				login(request, user)
				return redirect(home)
			else:
				return render(request, 'register.html', {'form':form, 'perr':"Passwords didn't match"})

	return render(request, 'register.html', {'form':form})


@login_required(login_url='/login/')
def addImage(request):
	form = addImageForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		if form.is_valid():
			image = form.save(commit=False)
			image.user = request.user
			image.likes = 0
			image.save()
			return redirect(home)
	return render(request, 'addImage.html', {'form':form})


def allImages(request):
	images = Image.objects.all()
	return render(request, 'profile.html', {'images':images, 'all':True})


def viewImage(request, image_id):
	context = {}
	context['image'] = Image.objects.get(id=image_id)
	context['form'] = commentForm()
	context['comments'] = Comment.objects.filter(image=context['image'])
	context['likes'] = Like.objects.filter(image_id=image_id).count()
	context['totalcomments'] = Comment.objects.filter(image_id=image_id).count()
	if request.user.is_authenticated():
		context['is_liked'] = Like.objects.filter(user=request.user, image_id=image_id).exists()
	return render(request, 'viewimage.html', context)


@login_required(login_url='/login/')
def comment(request, image_id):
	image = Image.objects.get(id=image_id)
	form = commentForm(request.POST)
	if form.is_valid():
		new_comment = form.save(commit=False)
		new_comment.user = request.user
		new_comment.image = image
		new_comment.save()

		return redirect(viewImage, image_id)


@login_required(login_url='/login/')
def editcomment(request, image_id, comment_id):
	to_change = Comment.objects.get(id=comment_id)
	to_change.cmnt = request.POST['edited-cmnt']
	to_change.commented = datetime.now()
	to_change.save()
	return redirect(viewImage, image_id)

@login_required(login_url='/login/')
def deletecomment(request, image_id, comment_id):
	comment = Comment.objects.get(id=comment_id)
	if comment.user == request.user or Image.objects.get(id=image_id).user == request.user:
		Comment.objects.get(id=comment_id).delete()
	return redirect(viewImage, image_id)


@login_required(login_url='/login/')
def like(request, image_id):
	if not Like.objects.filter(user=request.user, image_id=image_id).exists():
		image = Image.objects.get(id=image_id)
		image.likes += 1
		image.save()
		new_like = Like(user=request.user, image=image)
		new_like.save()
	return redirect(viewImage, image_id)

@login_required(login_url='/login/')
def dislike(request, image_id):
	if Like.objects.filter(user=request.user, image_id=image_id).exists():
		Like.objects.filter(user=request.user, image_id=image_id).delete()
	return redirect(viewImage, image_id)


def profile(request, username=''):
	context = {}
	context['this_user'] = User.objects.get(username=username)
	context['images'] = Image.objects.filter(user=context['this_user'])
	return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def deleteImg(request, image_id):
	image = Image.objects.get(id=image_id)
	if image.user == request.user:
		image.delete()
	return redirect(profile)

