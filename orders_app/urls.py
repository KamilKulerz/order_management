
from django.urls import path
from . import views

app_name = 'orders_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='orders'),
    path('orders/<str:pk>', views.order_detail, name='order'),
    path('orders/<str:pk>/update_items', views.order_detail_update, name='order-items-update'),
    path('orders/<str:pk>/update', views.order_update, name='orders-update'),
    path('orders/<str:pk>/delete', views.OrderDeleteView.as_view(), name='orders-delete'),
    path('orders/add', views.OrderCreateView.as_view(), name='orders-add'),

    path('ordereditem/add', views.OrderedItemCreateView.as_view(), name='ordereditem-add'),

    path('items/', views.ItemsList.as_view(), name='items'),
    path('items/<str:pk>/update', views.ItemUpdateView.as_view(), name='items-update'),
    path('items/<str:pk>/delete', views.ItemDeleteView.as_view(), name='items-delete'),
    path('items/add', views.ItemCreateView.as_view(), name='items-add'),

    path('customers/', views.CustomersList.as_view(), name='customers'),
    path('customers/<str:pk>/update', views.CustomerUpdateView.as_view(), name='customers-update'),
    path('customers/<str:pk>/delete', views.CustomerDeleteView.as_view(), name='customers-delete'),
    path('customers/add', views.CustomerCreateView.as_view(), name='customers-add'),

    path('categories/<str:pk>/update', views.CategoryUpdateView.as_view(), name='categories-update'),
    path('categories/<str:pk>/delete', views.CategoryDeleteView.as_view(), name='categories-delete'),
    path('categories/add', views.CategoryCreateView.as_view(), name='categories-add'),
    path('categories/', views.CategoriesList.as_view(), name='categories'),

]
