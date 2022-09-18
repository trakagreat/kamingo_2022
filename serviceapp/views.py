from unicodedata import category, name
import requests
from django.shortcuts import render, reverse
from .forms import ServiceForm, AddressForm
from .models import ServiceModel, ReviewModel, CategoryModel, ImageModel, Address
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse
from .filters import ServiceFilter
from .data.citieslist import cities
from django.contrib.auth.models import User
from django.db.models import Q




# Create your views here.
# Create your views here.
class HomePageView(View):
    def get(self , request):
        return render(request , 'serviceapp/home.html')

class FrontPageView(View , ):
    def get(self,request):
        context = {
            'filter':ServiceFilter(request.GET, queryset=ServiceModel.objects.all()),
            
        }
        return render(request, 'serviceapp/front_page.html', context)
        

class ServiceFormDesView(View):
    def get(self, request, slug):
        return render(request, 'serviceapp/service_form_description.html', {
            'slug': slug
        })

    def post(self, request, slug):
        des = request.POST.get('des')
        service = ServiceModel.objects.get(slug=slug)
        service.description = des
        service.save()
        return HttpResponseRedirect(reverse('front-page'))


class ServiceFormView(View):
    def get(self, request):
        categories = CategoryModel.objects.all()
        return render(request, 'serviceapp/service_form.html', {
            'cities': cities,
            'categories':categories,
        })

    def post(self, request):
        service = ServiceModel()
        service.title = request.POST.get('title')
        address = Address()
        address.address_line1 = request.POST.get('address1')
        address.address_line2 = request.POST.get('address2')
        address.pin_code = request.POST.get('pincode')
        address.city = request.POST.get('city')
        address.save()
        service.address = address
        service.cost = request.POST.get('cost')
        service.contact = request.POST.get('contact')
        service.description = request.POST.get('des')
        service.user = request.user

        category_name = request.POST.get('category')
        print(category_name)
        try:
            category = CategoryModel.objects.get(name=category_name)
        except:
            category = None
        service.category = category
        service.service_provider_name = request.POST.get('service_provider_name')
        service.slugify()
        service.save()
        images = request.FILES.getlist('images')
        for image in images:
            new_image = ImageModel(image=image, service=service)
            new_image.save()

        return HttpResponseRedirect(reverse('front-page'))
       

class ServiceDetailView(View):
    def get(self, request, slug):
        service = ServiceModel.objects.get(slug=slug)
        images = ImageModel.objects.filter(service=service)
        if request.user.is_authenticated:
            user_review = ReviewModel.objects.filter(service=service, user=request.user)
        else:
            user_review = None
        context = {
            'service': service,
            'user_review': user_review,
            'images': images,
        }

        return render(request, 'serviceapp/service_detail_page.html', context)

    def post(self, request, slug):
        rating = int(request.POST.get('rating'))
        content = request.POST.get('content')
        service = ServiceModel.objects.get(slug=slug)
        new_review = ReviewModel(rating=rating, content=content)
        new_review.service = service
        new_review.user = request.user
        new_review.save()
        return HttpResponseRedirect(reverse('service-detail-page', kwargs={
            'slug': slug,
        }))


class TestView(View):
    def get(self, request):
        pass

    def post(self, request):
        city = request.POST.get('city')
        return HttpResponse(city)


class PleaseLoginView(View):
    def get(self, requets):
        return render(requets, 'serviceapp/login_first.html')



class ServiceImageUploadView(View):
    def get(self, request ,slug, new_service):
        
        return render(request, 'serviceapp/service_form_images.html')

    def post(self, request):
        image = request.FILES.get('images')
        service = ServiceModel.objects.get(slug=request.POST.get('slug'))
        service.image = image
        service.save()




class PrivcayPolicyView(View):
    def get(self, request):

        return render(request, 'serviceapp/privacy_policy.html')

class Search_result_page(View):
    def post(self, request):
        all_services = ServiceModel.objects.all
        searched = request.POST['searched'].title()
        
        
        services = ServiceModel.objects.filter(Q(title__contains = searched) | Q(category__name__contains = searched))

        return render(request, 'serviceapp/search_result_page.html', {
            'searched':searched,
            'services':services,
            'all_services':all_services,
            'filter':ServiceFilter(request.GET, queryset=ServiceModel.objects.all()),

        })


