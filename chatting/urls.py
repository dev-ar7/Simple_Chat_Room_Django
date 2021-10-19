from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'<str:room_name>/', views.room, name='room'),
]
