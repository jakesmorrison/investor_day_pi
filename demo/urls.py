from django.conf.urls import url
from . import views

app_name = 'demo'
urlpatterns = [
    url(r'micron_slider/', views.micron_slider, name='micron_slider'),
    url(r'^change_led/$', views.change_led, name='change_led'),
]