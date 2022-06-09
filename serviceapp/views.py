import requests
from django.shortcuts import render, reverse
from .forms import ServiceForm, AddressForm
from .models import ServiceModel, ReviewModel, CategoryModel
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
        




    # def get(self, request, category='all', city='all'):
    #     if city == 'all' and category == 'all':
    #         services = ServiceModel.objects.all()
    #         default_cat = 'all'
    #     else:
    #         services = ServiceModel.objects.filter(address__city=city,category__name=category )
    #     categories = CategoryModel.objects.all()
    #     context = {
    #         'categories': categories,
    #         'cities': cities,
    #         'services': services,
    #     }
    #     return render(request, 'serviceapp/front_page.html', context)

    # def post(self, request, category, city):
    #     selected_category = request.POST.get('category')
    #     category = selected_category
    #     city = request.POST.get('city')
    #     # services = ServiceModel.objects.filter(category__name=selected_category)
    #     # f = ServiceFilter(request.GET, queryset=ServiceModel.objects.all())
    #     # categories = CategoryModel.objects.all()
    #     # context = {
    #     #     'filter': f,
    #     #     'categories': categories,
    #     #     'cities': cities,
    #     #     'services': services
    #     #
    #     # }
    #     return HttpResponseRedirect(reverse('front-page', kwargs={
    #         'city':city,
    #         'category': category,
    #     }))


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
        service = ServiceForm(request.POST, request.FILES)
        address = AddressForm(request.POST)
        if service.is_valid():
            new_service = service.save(commit=False)
            new_address = address.save(commit=False)
            new_address.city = request.POST.get('city')
            new_address.save()
            new_service.address = new_address
            new_service.slugify()
            new_service.user = request.user
            new_service.save()
            slug = new_service.slug
            return HttpResponseRedirect(reverse('service_form_des_url', kwargs={
                'slug': slug,
            }))
        else:
            return render(request, 'serviceapp/service_form.html', {
                "form": service,
                'address_form': address,
                'cities': cities,
            })


class ServiceDetailView(View):
    def get(self, request, slug):
        service = ServiceModel.objects.get(slug=slug)
        if request.user.is_authenticated:
            user_review = ReviewModel.objects.filter(service=service, user=request.user)
        else:
            user_review = None
        context = {
            'service': service,
            'user_review': user_review,
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
        return render(request, 'serviceapp/test.html', {
            'cities': cities,
        })

    def post(self, request):
        city = request.POST.get('city')
        return HttpResponse(city)


class PleaseLoginView(View):
    def get(self, requets):
        return render(requets, 'serviceapp/login_first.html')
