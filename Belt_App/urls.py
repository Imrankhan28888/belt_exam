from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('thoughts', views.thoughts),
    path('post_thought', views.post_thought),
    path('thought/<int:id>', views.show_thought),
    path('delete/<int:id>', views.delete_thought),
    path("favorite/<int:thought_id>", views.favorite),
    path("unfavorite/<int:thought_id>", views.unfavorite),
    
  
]