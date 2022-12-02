from django.urls import path
from . import views

urlpatterns = [
    path('nlp/',views.nlp,name='nlp'),
]