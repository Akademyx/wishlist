from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^main$', views.main), #GET ROUTES
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/(?P<id>\d+)$', views.wish_item),
    url(r'^wish_items/create$', views.create_form),
    #POST routes
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_item$', views.add_item),
    url(r'^delete_item/(?P<id>\d+)$', views.delete),
    url(r'^delete_item/mine/(?P<id>\d+)$', views.delete_mine),
    url(r'^join/(?P<id>\d+)$', views.join)
]
