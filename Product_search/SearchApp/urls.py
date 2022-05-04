from django.urls import path
from . import views
from .webhook import WebhookApi

urlpatterns = [
    path('', views.login),                              # https://3itest2.pagekite.me/login
    path('final', views.final),                         # https://3itest2.pagekite.me/final
    path('installation', views.installation), 
    path('uninstall', WebhookApi.webhook_uninstall),    # https://3itest2.pagekite.me/uninstall
    path("get_installation",views.get_installation),
    path('products_list',views.products_list),
    path('search_product_list',views.search_product_list)
    # path('customer', views.customer),                   # https://3itest2.pagekite.me/customer
    # path('activation_url',views.activation_url)         # https://3itest2.pagekite.me/activation_url 
    
]