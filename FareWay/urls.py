from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^registration/register/$', views.register, name='register'),
    url(r'^registration/register/success/$', views.registration_complete, name='registration_complete'),
    url(r'^attraction/(?P<pk>\d+)/$', views.attraction_details, name='attraction_details'),
    url(r'^attraction/$',views.attractions, name='attractions'),
]