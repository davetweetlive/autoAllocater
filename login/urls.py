from django.urls import path
from . import views

urlpatterns = [
	# /www_dave/
	path('', views.index, name='index'),
    
    # /www_dave/home
    path('home/', views.home, name='home'),
]