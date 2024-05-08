from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.details, name='details'),
    path("sellers/", views.sellers, name='seller'),
    path("sellers/<int:id>", views.seller_details, name='seller_details'),
    path("init_db/", views.init, name='initialize')
]