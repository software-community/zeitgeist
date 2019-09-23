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
from . import views

urlpatterns = [
    path('', views.verzeo_home, name = "verzeo_home"),

    path('arts_commerce/', views.arts_commerce, name = "arts_commerce"),
    path('arts_commerce/advertising/', views.advertising, name = "advertising"),
    path('arts_commerce/content/', views.content, name = "content"),
    path('arts_commerce/digital/', views.digital, name = "digital"),
    path('arts_commerce/hr/', views.hr, name = "hr"),
    path('arts_commerce/journalism/', views.journalism, name = "journalism"),
    path('arts_commerce/lean/', views.lean, name = "lean"),
    path('arts_commerce/marketing/', views.marketing, name = "marketing"),
    path('arts_commerce/photo/', views.photo, name = "photo"),
    path('arts_commerce/psychology/', views.psychology, name = "psychology"),
    path('arts_commerce/shortfilm/', views.shortfilm, name = "shortfilm"),

    path('bio/', views.bio, name = "bio"),
    path('bio/nano', views.nano, name = "nano"),

    path('civil/', views.civil, name = "civil"),
    path('civil/autocad/', views.autocad, name = "autocad"),
    path('civil/construction/', views.construction, name = "construction"),

    path('cse/', views.cse, name = "cse"),
    path('cse/ai/', views.ai, name = "ai"),
    path('cse/azure/', views.azure, name = "azure"),
    path('cse/bc/', views.bc, name = "bc"),
    path('cse/ds/', views.ds, name = "ds"),
    path('cse/eh/', views.eh, name = "eh"),
    path('cse/machine/', views.machine, name = "machine"),
    path('cse/web/', views.web, name = "web"),

    path('ece/', views.ece, name = "ece"),
    path('ece/hybrid/', views.hybrid, name = "hybrid"),
    path('ece/iot/', views.iot, name = "iot"),
    path('ece/robotics/', views.robotics, name = "robotics"),

    path('management/', views.management, name = "management"),
    path('management/blockchain/', views.blockchain, name = "blockchain"),
    path('management/finance_stock/', views.finance_stock, name = "finance_stock"),

    path('mech/', views.mech, name = "mech"),
    path('mech/autocadmech/', views.autocadmech, name = "autocadmech"),
    path('mech/car/', views.car, name = "car"),
    path('mech/catia/', views.catia, name = "catia"),
    path('mech/hybridmech/', views.hybridmech, name = "hybridmech"),
    path('mech/icenginee/', views.icenginee, name = "icenginee"),
]
