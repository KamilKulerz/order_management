
from django.urls import path
from . import views

app_name = 'orders_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.OrdersList.as_view(), name='orders'),
    path('add_orders/', views.OrderCreateView.as_view(), name='add_orders'),
    path('items/', views.ItemsList.as_view(), name='items'),
    path('add_items/', views.ItemCreateView.as_view(), name='add_items'),
    path('customers/', views.CustomersList.as_view(), name='customers'),
    path('add_customers/', views.CustomerCreateView.as_view(), name='add_customers'),
    path('categories/', views.CategoriesList.as_view(), name='categories'),

]
