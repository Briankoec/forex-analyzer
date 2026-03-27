from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('pair/<int:pair_id>/', views.pair_detail, name='pair_detail'),
    path('pair/<int:pair_id>/refresh/', views.refresh_pair, name='refresh_pair'),
    path('api/pair/<int:pair_id>/data/', views.api_pair_data, name='api_pair_data'),
    path('api/pair/<int:pair_id>/signals/', views.api_signals, name='api_signals'),
    path('api/create-pair/', views.create_pair, name='create_pair'),
]
