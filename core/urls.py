from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView.as_view()),
    path('get/departments/',views.GetAllDepartment.as_view()),
    path('get/cakes/<str:id>/',views.GetAllCakes.as_view())
]
