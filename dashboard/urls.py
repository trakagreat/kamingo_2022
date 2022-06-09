from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/<int:pk_service>', views.ServiceUpdateView.as_view(), name='service_edit_url'),
    path('<int:pk>/<int:pk_service>/des', views.ServiceDesUpdateView.as_view(), name='service_des_edit_url'),
    path('<int:pk>', views.DashboardView.as_view(), name='dashboard_url'),

]
