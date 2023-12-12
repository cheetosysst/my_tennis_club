from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("members/", views.members, name="members"),
    path("members/details/<int:id>", views.details, name="details"),
    path("testing/", views.testing, name="testing"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="register"),
    path("addcourt/", views.add_court, name="register"),
    path("court/", views.court, name="register"),
    path("court/details/<str:id>", views.details_court, name="details_court"),
    path("court/book/<str:id>", views.book_court, name="details_court"),
    path("court/book/", views.books, name="details_court"),
]
