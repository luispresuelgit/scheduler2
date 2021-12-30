from django.urls import path
from activities import views

urlpatterns = [
    path('properties/', views.property_list),
    path('properties/<int:property_id>/', views.property_detail),
    path('activities/', views.activity_list),
    path('activities/<int:activity_id>/', views.activity_detail),
    path('activities/<int:activity_id>/survey/', views.survey_list),
    path('activities/<int:activity_id>/survey/<int:survey_id>/', views.survey_detail),
]