from django.urls import path
from . import views

urlpatterns = [
    # your existing monastery routes
    path('<int:pk>/weather/', views.monastery_weather, name='monastery-weather'),
]
