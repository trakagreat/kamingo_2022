from django.urls import path

from serviceapp.filters import ServiceFilter
from . import views
from django_filters.views import object_filter
from serviceapp.models import ServiceModel

urlpatterns = [
    # url for filter
    path('', views.HomePageView.as_view(), name='home-page'),
    path('service', views.FrontPageView.as_view(), name='front-page'),
    path('service-form', views.ServiceFormView.as_view(), name='service_form_url'),
    path('service-form', views.PleaseLoginView.as_view(), name='login_first_url'),
    path('service-form/<slug:slug>/description', views.ServiceFormDesView.as_view(), name='service_form_des_url'),
    path('<slug:slug>', views.ServiceDetailView.as_view(), name='service-detail-page'),
    path('image', views.ServiceImageUploadView.as_view(), name='service_image_upload_url'),
    path('test', views.TestView.as_view(), name='test'),
    path('legal/privacy-policy', views.PrivcayPolicyView.as_view()),
    path('search/', views.Search_result_page.as_view(), name='search_result_page'),

    
]
# 