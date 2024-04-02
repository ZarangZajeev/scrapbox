"""
URL configuration for scrapboxapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrapboxapp import views
from django.conf import settings
from django.conf.urls.static import static
from scrapboxapp.views import product_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path("scrapbox/register",views.SignUpView.as_view(),name="signup"),
    path("",views.LandingView.as_view(),name="landing"),
    path("signin",views.SigninView.as_view(),name="signin"),
    path("scrapbox/signout",views.SignoutView.as_view(),name="signout"),
    path("scrapbox/index",views.IndexView.as_view(),name="index"),
    path("scrapbox/profile-edit/<int:pk>/change",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("scrapbox/<int:pk>",views.ProfileDetailView.as_view(),name="profile"),
    path("scrapbox/scrap/add",views.ScrapAddView.as_view(),name="scrap-add"),
    path("scrapbox/scrap/category",views.CategoryAddView.as_view(),name="category"),
    path("scrapbox/scrap/<int:pk>",views.ScrapDetailView.as_view(),name="scrap-detail"),
    path("scrapbox/<int:pk>/change",views.ScrapUpdateView.as_view(),name="scrap-update"),
    path("scrapbox/<int:pk>/remove",views.ScrapDelateView.as_view(),name="scrap-delete"),
    path("scrapbox/<int:pk>/wishlist",views.WishlistAddView.as_view(),name='wishlist'),
    path("scrapbox/wishlist",views.WishlistView.as_view(),name="wishlistview"),
    path("scrapbox/all-bids",views.BidRequestView.as_view(),name="all-bids"),
    path("scrapbox/<int:pk>/bidrequest",views.AllBidsView.as_view(),name="bid-request"),
    path('search',product_search,name="pro-search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)