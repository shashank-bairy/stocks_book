from django.urls import path

from .views import index

urlpatterns = [
    path('stocks/search/<str:input>/', index)
]