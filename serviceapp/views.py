import requests
from django.shortcuts import render, reverse
from .forms import ServiceForm, AddressForm
from .models import ServiceModel, ReviewModel, CategoryModel, ImageModel
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse
from .filters import ServiceFilter
from .data.citieslist import cities



# Create your views here.
# Create your views here.


class FrontPageView(View):
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
        service_form = ServiceForm()
        address_form = AddressForm()
        return render(request, 'serviceapp/service_form.html', {
            "form": service_form,
            "address_form": address_form,
            'cities': cities,
        })

    def post(self, request):
        service = ServiceForm(request.POST)
        address = AddressForm(request.POST)
        if service.is_valid():          
            new_service = service.save(commit=False)
            new_address = address.save(commit=False)
            new_address.city = request.POST.get('city')
            new_address.save()
            new_service.address = new_address
            new_service.user = request.user
            new_service.slugify()
            new_service.description = request.POST.get('des')
            new_service.save()
            images = request.FILES.getlist('images')
            for image in images:
                new_image = ImageModel(image=image, service=new_service)
                new_image.save()
    
            return HttpResponseRedirect(reverse('front-page'))
        else:
            return render(request, 'serviceapp/service_form.html', {
                "form": service,
                'address_form': address,
                'cities': cities,
            })

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
        