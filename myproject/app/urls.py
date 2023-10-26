from django.urls import path

from . import views
from registration import views as view_registration


urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.all_product_add_user, name='cart'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<int:product_id>/', views.add_product_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_product_from_cart, name='delete_from_cart'),
    path('login/', view_registration.login_user, name='login'),
    path('logout/', view_registration.logout_user, name='logout'),
    path('register/', view_registration.sign_up, name='register'),
    path('edit_profile/', view_registration.edit_profile, name='profile'),
]
