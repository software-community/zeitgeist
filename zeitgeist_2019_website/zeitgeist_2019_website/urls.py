"""zeitgeist_2019_website URL Configuration

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

handler404 = 'main_page.views.error_404'
handler500 = 'main_page.views.under_maintainance'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main_page.urls")),
    path('campus_ambassador/', include("campus_ambassador.urls")),
    # path('TSP/',include("TSP.urls")),
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon-precomposed.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon-120x120-precomposed.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon-120x120.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon-152x152.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png'))),
    path('apple-touch-icon-152x152-precomposed.png',RedirectView.as_view(url=staticfiles_storage.url('main_page/img/logo/favicon.png')))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
