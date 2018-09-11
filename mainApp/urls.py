from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('influencer/add/', views.InfluencerCreate, name='influencer-add'),
    path('influencer/<uuid:pk>/', views.InfluencerUpdate, name='influencer-update'),
    path('influencer/<uuid:pk>/delete/', views.InfluencerDelete.as_view(), name='influencer-delete'),
    path('influencer/add/csv', views.InfluencerCreateCSV, name='influencer-add-csv'),

]
