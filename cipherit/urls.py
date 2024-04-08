"""cipherit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from cipher import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('message/',views.message,name='message'),
    path('index/',views.index,name='index'),
    path('inbox/',views.inbox,name='inbox'),
    path('inbox1/',views.inbox1,name='inbox1'),
    path('draft/',views.draft,name='draft'),
    path('draft1/',views.draft1,name='draft1'),
    path('sent/',views.sent,name='sent'),
    path('question/',views.question,name='question'),
   # path('sent1/',views.sent1,name='sent1'),
    path('delete/',views.delete,name='delete'),
    path('changeimage/',views.changeimage,name='changeimage'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('forgotpwd/',views.forgotpwd,name='forgotpwd'),
    path('feedback/',views.feedback,name='feedback'),
    path('',views.common_home,name='common_home'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('user_home/',views.user_home,name='user_home'),
    path('userbase/',views.userbase,name='userbase'),
    path('userview/',views.userview,name='userview'),
    path('viewfeedback/',views.viewfeedback,name='viewfeedback'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('result/',views.result,name='results'),
    path('download/',views.download,name='download'),

]+staticfiles_urlpatterns()
