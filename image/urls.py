from django.conf.urls import url
from .import views
from django.contrib.auth.views import logout

urlpatterns = [
	url(r'^$', views.home),
	url(r'^login/', views.logIn),  
	url(r'^register/', views.register),   
	url(r'^logout/$', logout, {'next_page': '/'}),
	url(r'^add-image/$', views.addImage),
	url(r'^all-images/$', views.allImages),
	url(r'^image/(?P<image_id>[0-9]+)/$', views.viewImage),
	url(r'^image/(?P<image_id>[0-9]+)/comment/$', views.comment),
	url(r'^image/(?P<image_id>[0-9]+)/like/$', views.like),
	url(r'^image/(?P<image_id>[0-9]+)/dislike/$', views.dislike),
	url(r'^image/edit-comment/(?P<image_id>[0-9]+)-(?P<comment_id>[0-9]+)/$', views.editcomment),
	url(r'^image/delete-comment/(?P<image_id>[0-9]+)-(?P<comment_id>[0-9]+)/$', views.deletecomment),
	url(r'^profile(?:/(?P<username>[a-zA-Z]+))?/$', views.profile),
	url(r'^image/delete-(?P<image_id>[0-9]+)/$', views.deleteImg),
]