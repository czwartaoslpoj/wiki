from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.showEntry, name="wiki/entry"),
    path("results", views.search, name="results"),
    path("add", views.addEntry, name="add")
]
