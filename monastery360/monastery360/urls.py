from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monasteries.views import (
    MonasteryViewSet, ArchiveViewSet,
    MonkViewSet, MonkSessionViewSet, MonkSessionApplicationViewSet,monastery_weather,monastery_360_tour,MonasteryEventsList, BookEventSeat
)
from monasteries import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from monasteries.views import static_map
from monasteries.views import monastery_route_pdf
from django.urls import path
from monasteries.views import monastery_inside_virtual_tour






router = DefaultRouter()
router.register(r'monasteries', MonasteryViewSet)
router.register(r'archives', ArchiveViewSet)
router.register(r'monks', MonkViewSet)
router.register(r'sessions', MonkSessionViewSet)
router.register(r'applications', MonkSessionApplicationViewSet)



# sikkim_tourism/urls.py



    


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/monasteries/<int:pk>/weather/", monastery_weather, name="monastery-weather"),
    path("api/static-map/", static_map, name="static_map"),
    path("api/monasteries/<int:monastery_id>/route_pdf/", monastery_route_pdf),
    path('monastery/<int:monastery_id>/360-tour/', views.monastery_360_tour, name='monastery_360_tour'),
    path('monastery/<int:monastery_id>/360-viewer/', views.monastery_360_viewer, name='monastery_360_viewer'),
    # path('monastery/<int:monastery_id>/streetview-embed/', views.monastery_streetview_embed, name='monastery_streetview_embed'),
    path("api/monasteries/<int:monastery_id>/inside-tour/", monastery_inside_virtual_tour, name="monastery_inside_tour"),
    path("api/monasteries/<int:monastery_id>/events/", MonasteryEventsList.as_view(), name="monastery-events"),
    path("api/events/<int:event_id>/book/", BookEventSeat.as_view(), name="book-event"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


