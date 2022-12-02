from django.urls import path
from . import views

urlpatterns = [
    path('search/',views.search,name='search'),
    path('search/search_results',views.search_results,name='search_results'),
    path('search/search_results/search_field_info/<str:field_name>/',views.search_field_info,name='search_field_info'),
    path('search/search_results/search_field_info/field_summary/<str:field_name>/',views.field_summary,name='field_summary'),
    path('search_for_topic/',views.search_for_topic,name='search_for_topic'),
    path('search_for_topic/search_topic_results',views.search_topic_results,name='search_topic_results'),
    path('search_for_document/search_document_results/',views.search_document_results,name='search_document_results'),
    path('search_for_document/',views.search_for_document,name='search_for_document'),
    path('search_for_author/',views.search_for_author,name='search_for_author'),
    path('search/field_example/<str:field_name>/',views.field_example,name='field_example'),
    path('search/field_example/topic_info/<int:id>/',views.topic_info,name='topic_info'),
    path('search_for_topic/topic_example',views.topic_example,name='topic_example'),
    path('search/field_example/field_example_authors/<str:field_name>/',views.field_example_authors,name='field_example_authors'),
    path('search/field_example/field_example_authors/author_info/<int:id>/',views.author_info,name='author_info'),
    path('search/field_example/field_example_authors/all_authors/<str:field_name>/',views.all_authors,name='all_authors'),
    path('search/field_example/all_topics/<str:field_name>/',views.all_topics,name='all_topics'),
    path('search/topic_example/all_documents/<int:id>/',views.all_documents,name='all_documents'),
    #path('search/field_example/topic_info/<int:id>/all_documents/<int:id>/',views.all_documents,name='all_documents'),
    path('search/topic_example/all_documents/document_info/<int:id>/',views.document_info,name='document_info')
 ]