"""
URL configuration for monastery360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import routers
from monasteries.views import MonasteryViewSet
from monasteries.views import ArchiveViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from monasteries.views import MonkViewSet, MonkSessionViewSet, MonkSessionApplicationViewSet

router = routers.DefaultRouter()
router.register(r'monasteries', MonasteryViewSet)


router.register(r'archives', ArchiveViewSet)  # new route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/monasteries/', include('monasteries.urls')),

]



router = DefaultRouter()
router.register(r'monks', MonkViewSet)
router.register(r'sessions', MonkSessionViewSet)
router.register(r'applications', MonkSessionApplicationViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/monasteries/", include("monasteries.urls")),  # monasteries + weather + archives
    path("api/", include(router.urls)),                     # monks/sessions/applications here
]






if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)