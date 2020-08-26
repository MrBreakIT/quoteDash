from django.urls import path, include
from . import views

urlpatterns = [
    ###################################
    #       Register/Login
    ###################################
    path('', views.index),
    path("login", views.login),    
    path("home", views.home),
    path("registerUser", views.registerUser),
    # path("register", views.register),
    path("logout", views.logout),
    ###################################
    #       quoteHomepage
    ###################################
    path("userQuotes", views.userQuotes),
    path("delete/<int:quotesID>", views.deleteQuote),
    path("addAuthorQuote", views.addAuthorQuote),
    path('editUserAcct/<int:userID>', views.editUserAcct),
    path('updateUser/<int:userID>', views.updateUser),
    path('loggedUserQuotes/<int:userID>', views.loggedUserQuotes),


]