from django.urls import path
from . import views


urlpatterns=[

path('', views.dashboard, name='dashboard'),
path('Settings', views.Setting, name='Settings'),
path('setting_security', views.setting_security, name='setting_security'),



#product related
path('add_product', views.add_product, name='add_product'),
path('delete_product', views.delete_product, name='delete_product'),
path('add_image', views.add_image, name='add_image'),






]
