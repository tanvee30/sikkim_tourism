from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monasteries.views import (
    MonasteryViewSet, ArchiveViewSet,
    MonkViewSet, MonkSessionViewSet, MonkSessionApplicationViewSet,
    monastery_weather, MarketListView, MarketDetailView, get_route_to_market,
    static_map, monastery_route_pdf)

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'monasteries', MonasteryViewSet)
router.register(r'archives', ArchiveViewSet)
router.register(r'monks', MonkViewSet)
router.register(r'sessions', MonkSessionViewSet)
router.register(r'applications', MonkSessionApplicationViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/monasteries/<int:pk>/weather/", monastery_weather, name="monastery-weather"),
    path("api/static-map/", static_map, name="static_map"),
    path("api/monasteries/<int:monastery_id>/route_pdf/", monastery_route_pdf, name="monastery_route_pdf"),
    path("api/markets/", MarketListView.as_view(), name="market-list"),
    path("api/markets/<int:pk>/", MarketDetailView.as_view(), name="market-detail"),
    path("api/markets/<int:pk>/route/", get_route_to_market, name="market-route"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




