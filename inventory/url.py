from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', views.login_user, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('', views.login_user, name='login'),
    path('accounts/profile/', views.index, name='home'),
    path('additem', views.additem, name='additem'),
    path('voucherinfo', views.voucherinfo, name='voucherinfo'),
    path('voucherlist', views.voucherlist, name='voucherlist'),
    path('createvoucher', views.createvoucher, name='createvoucher'),

]