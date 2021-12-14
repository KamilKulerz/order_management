
from django.urls import path
from . import views

app_name = 'orders_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='orders'),
    # path('orders/', views.OrdersList.as_view(), name='orders'),
    path('orders/<str:pk>', views.order_detail, name='order'),
    path('orders/update_items/<str:pk>',
         views.order_detail_update, name='order_detail_update'),
    path('orders/update/<str:pk>', views.order_update, name='order_update'),
    #     path('orders/<str:pk>', views.OrderDetail.as_view(), name='order'),
    path('orders/delete/<str:pk>',
         views.OrderDeleteView.as_view(), name='delete_order'),
    path('add_orders/', views.OrderCreateView.as_view(), name='add_orders'),
    path('add_ordereditem/', views.OrderedItemCreateView.as_view(),
         name='add_ordereditem'),
    path('items/', views.ItemsList.as_view(), name='items'),
    path('add_items/', views.ItemCreateView.as_view(), name='add_items'),
    path('customers/', views.CustomersList.as_view(), name='customers'),
    path('customers/<str:pk>/update',
         views.CustomerUpdateView.as_view(), name='customers-update'),
    path('customers/<str:pk>/delete',
         views.CustomerDeleteView.as_view(), name='customers-delete'),
    path('add_customers/', views.CustomerCreateView.as_view(), name='add_customers'),
    path('categories/<str:pk>/update',
         views.CategoryUpdateView.as_view(), name='categories-update'),
    path('categories/<str:pk>/delete',
         views.CategoryDeleteView.as_view(), name='categories-delete'),
    path('add_categories/', views.CategoryCreateView.as_view(),
         name='add_categories'),
    path('categories/', views.CategoriesList.as_view(), name='categories'),

]
