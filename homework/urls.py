"""homework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views import static
from django.conf import settings
from django.conf.urls import url
from django.urls import path
from web import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('order/', views.create_order, name='create_order'),
    path('order/<str:order_id>', views.delete_order, name='delete_order'),
    path('stat/order', views.get_order_stat, name='get_order_stat'),
    path('stat/shop', views.get_shop_stat, name='get_shop_stat'),
    url(r'^static/(?P<path>.*)$', static.serve,
      {'document_root': settings.STATICFILES_DIRS[0]}, name='static'),
]
