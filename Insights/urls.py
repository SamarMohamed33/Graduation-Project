from django.urls import path
from . import views

urlpatterns = [
    path('insights_authors/', views.insights_authors, name='insights_authors'),
    path('insights_authors/table', views.insights_authors_table, name='insights_authors_table'),
    path('insights_keyphrases/', views.insights_keyphrases, name='insights_keyphrases'),
    path('insights_keyphrases/chart/<int:id>/',views.insights_keyphrases_chart,name='insights_keyphrases_chart'),
 ]