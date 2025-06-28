from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_history_view, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('profile/update-email/', views.update_email_view, name='update_email'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('details/', views.account_detail_view, name='account_detail'),

]
