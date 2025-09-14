from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonkViewSet, MonkSessionViewSet, MonkSessionApplicationViewSet

router = DefaultRouter()
router.register(r'monks', MonkViewSet)
router.register(r'sessions', MonkSessionViewSet)
router.register(r'applications', MonkSessionApplicationViewSet)

urlpatterns = [
    # your existing monastery routes
    path('<int:pk>/weather/', views.monastery_weather, name='monastery-weather'),
    path('<int:pk>/archives/', views.MonasteryArchivesView.as_view(), name='monastery-archives'),
    path("", include(router.urls)),
]





