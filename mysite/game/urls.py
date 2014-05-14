from django.conf.urls import patterns, include, url

from game import views

urlpatterns = patterns('',
                       url(r'^lure$', views.lure, name='lure'),
                       url(r'^make_move$', views.make_move, name='make_move'),
                       url(r'^$', views.home, name='home'),
                       )
