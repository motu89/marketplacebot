from django.urls import path
from . import views


urlpatterns=[

path('', views.dashboard, name='dashboard'),
path('Settings', views.Setting, name='Settings'),
path('setting_security', views.setting_security, name='setting_security'),

# Facebook account management
path('facebook_accounts', views.facebook_accounts, name='facebook_accounts'),
path('save_fb_account', views.save_fb_account, name='save_fb_account'),
path('delete_fb_account/<int:account_id>/', views.delete_fb_account, name='delete_fb_account'),
path('fb_accounts', views.fb_accounts, name='fb_accounts'),  # Legacy route for backward compatibility
path('publish_with_account/<int:account_number>/', views.publish_with_account, name='publish_with_account'),

#product related
path('add_product', views.add_product, name='add_product'),
path('delete_product', views.delete_product, name='delete_product'),
path('add_image', views.add_image, name='add_image'),
path('upload_images', views.upload_images, name='upload_images'),





]
