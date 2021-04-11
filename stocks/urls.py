from django.urls import path

from .views import StocksSearchView

urlpatterns = [
    path('search/<str:input>/', StocksSearchView.as_view())
]