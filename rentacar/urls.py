from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('caradd/', views.caradd, name='caradd'),
    path('carlist/', views.carlist, name='carlist'),
    path('carrent/<int:pk>/', views.carrent, name='carrent'),
]
