from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView.as_view()),
    path('login/admin/',views.AdminLogin.as_view()),
    path('get/departments/',views.GetAllDepartment.as_view()),
    path('get/cakes/<str:id>/',views.GetAllCakes.as_view()),
    path('order/',views.PostOrder.as_view()),
    path('order/pending/',views.AdminPendingCakes.as_view()),
    path('order/process/',views.AdminProccessingCakes.as_view()),

]
