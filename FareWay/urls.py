from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^registration/register/$', views.register, name='register'),
    url(r'^registration/register/success/$', views.registration_complete, name='registration_complete'),
    url(r'^attraction/(?P<pk>\d+)/$', views.attraction_details, name='attraction_details'),
    url(r'^attraction/$',views.attractions, name='attractions'),
    url(r'^routes/$', views.RoutesView.as_view(), name='routes'),
    url(r'^attractions/$', views.attractions, name='attractions'),
    url(r'^routes/(?P<route_pk>(([0-9]+)|(empty)))/$', views.route_config, name='route_config'),
    url(r'^routes/remove/(?P<route_pk>[0-9]+)/$', views.remove_route, name='remove_route'),
    url(r'^routes/new/$', views.SamleRoutesView.as_view(), name='new_route'),
    url(r'^routes/update/$', views.update_route, name='update_route'),
    url(r'^categories/$', views.categories, name='categories'),
]