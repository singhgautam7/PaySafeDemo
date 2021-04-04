"""PaysafeTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from payments import views as payment_views
from payments import apis as payment_apis

urlpatterns = [

    # Payment urls
    path('', payment_views.home, name="home"),
    path('signup/', payment_views.signup, name='signup'),
    path('login/', payment_views.login_view, name='login'),
    path('logout/', payment_views.logout_view, name='logout'),
    path('api-auth/', include('rest_framework.urls')),

    # API urls
    path('api/payment/process/amount/<int:amount>/token/<slug:token>/', payment_apis.process_payment,
         name='api-process'),

    # Admin url
    path('admin/', admin.site.urls),

]
