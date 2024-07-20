from django.urls import path, include
from myApp import views
from myApp.iris.views import irisData, insertData, updateData, deleteData

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("iris/", irisData, name="iris"),
    path("insert/", insertData, name="insertData"),
    path("update/<int:id>/", updateData, name="updateData"),
    path("delete/<int:id>/", deleteData, name="deleteData"),
]
