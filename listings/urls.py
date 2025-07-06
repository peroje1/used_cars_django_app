from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('add/', views.add_car, name='add_car'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),  # NEW
    path('car/<int:car_id>/delete/', views.delete_car, name='delete_car'),  # NEW
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)