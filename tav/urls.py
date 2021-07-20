"""tav URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from tav.views import choosefile, showresults, showayuda

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', choosefile, name = 'choosefile'  ),
    url(r'^showresults/$', showresults , name = 'showresults' ),
    url(r'^showayuda/$', showayuda, name = 'showayuda'   ),
    url(r'^choosefile/$', choosefile, name = 'choosefile'   ),

]

  