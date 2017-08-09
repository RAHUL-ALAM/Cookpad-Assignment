from django.contrib.auth.models import User
from django import forms
from .models import Image, Comment

class userRegForm(forms.ModelForm):
	
	username = forms.CharField(widget=forms.TextInput(attrs=
		{'name':"username",'id':"username",'class':"form-control",'placeholder':"Desired Username"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'name':'password','id':'password','class':'form-control','placeholder':'Password'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'name':'retype_password','id':'r_password','class':'form-control','placeholder':'Retype Password'}))

	class Meta:
		model = User
		fields = ['username', 'password', 'password2']


class logForm(forms.Form):
	username = forms.CharField(max_length=15,widget = forms.TextInput(attrs=
		{'name':"username",'id':"username",'class':"form-control",'placeholder':"Username"}))
	password = forms.CharField(max_length=15,widget = forms.PasswordInput(attrs=
		{'name':'password','id':'password','class':'form-control','placeholder':'Password'}))

class addImageForm(forms.ModelForm):

	description = forms.CharField(widget=forms.Textarea(attrs=
		{'name':"description",'id':"descrip",'class':"form-control",'placeholder':"description",'rows':"3"}))
	img = forms.FileField(widget= forms.ClearableFileInput(attrs={'id':"img", 'class':"form-control"}))

	class Meta:
		model = Image
		fields = ['description', 'img']

class commentForm(forms.ModelForm):

	cmnt = forms.CharField(widget=forms.Textarea(attrs={'name':"cmnt",'id':"cmnt",'class':"form-control",'rows':"3"}))

	class Meta:
		model = Comment
		fields = ['cmnt']
			