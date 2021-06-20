from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name='index'),
    path('favourite', views.favourite, name='favourite'),
    path('vote',views.vote,name = 'vote')

]