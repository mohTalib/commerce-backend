from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.createlist, name="create"),
    path("displaycate", views.displaycate, name="displaycate"),
    path("Listing/<int:id>", views.Listing, name="Listing"),
    path("Removefromwhatchlist/<int:id>", views.Removefromwhatchlist, name="Removefromwhatchlist"),
    path("Addtowhatchlist/<int:id>", views.Addtowhatchlist, name="Addtowhatchlist"),
    path('displaywatch', views.displaywatch, name=views.displaywatch),
    path('addcomment/<int:id>', views.addcomment, name="addcomment"),
    path('addbid', views.addbid, name="bid"),
    path('closeauic', views.closeauic, name="closeauic"),
]
