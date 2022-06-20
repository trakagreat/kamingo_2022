from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from .models import ServiceModel ,CategoryModel , ImageModel
from django.views import View
from django.contrib.auth.models import User
from serviceapp.forms import AddressForm
from .forms import EditServiceForm
from serviceapp.data.citieslist import cities
from django.http import HttpResponseRedirect


# Create your views here.

class ServiceUpdateView(View):
    def get(self, request, pk, pk_service):
        service = ServiceModel.objects.get(pk=pk_service)
        categories = CategoryModel.objects.all()
        context = {
            'pk': pk,
            'pk_service': pk_service,
            'service': service,
            'cities': cities,
            'categories': categories
        }
        return render(request, 'dashboard/service_edit.html', context)

    def post(self, request, pk, pk_service):
        images = request.FILES.getlist('images')
        service = ServiceModel.objects.get(pk=pk_service)
        service.title = request.POST.get('title')
        address = service.address
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2')
        address.pin_code = request.POST.get('pin_code')
        address.city = request.POST.get('city')
        address.save()
        service.cost = request.POST.get('cost')
        service.contact = request.POST.get('contact')

        category_name = request.POST.get('category')
        category = CategoryModel.objects.get(name=category_name)
        service.category = category
        service.service_provider_name = request.POST.get('service_provider_name')
        service.slugify()
        service.save()
        
        print(len(images))
        if len(images) > 0:
            images_delete = ImageModel.objects.filter(service=service)
            for image in images_delete:
                image.delete()
            for image in images:
                new_image = ImageModel(image=image , service=service)
                new_image.save()
        service = ServiceModel.objects.get(pk=pk_service)
        context = {
            'pk': pk,
            'pk_service': pk_service,
            'service': service,


        }
        return HttpResponseRedirect(reverse('service_des_edit_url', kwargs={
            'pk': pk,
            'pk_service': pk_service,
        }))


class DashboardView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        services = ServiceModel.objects.filter(user=user)
        context = {
            'services': services
        }
        return render(request, 'dashboard/user_dasboard_main.html', context)


class ServiceDesUpdateView(View):
    def get(self, request, pk, pk_service):
        service = ServiceModel.objects.get(pk=pk_service)
        context = {
            'pk': pk,
            'pk_service': pk_service,
            'service': service
        }
        return render(request, 'dashboard/service_edit_description.html', context)

    def post(self, request, pk, pk_service):
        service = ServiceModel.objects.get(pk=pk_service)
        service.description = request.POST.get('des')
        service.save()

        return HttpResponseRedirect(reverse('dashboard_url', kwargs={
            'pk': pk,

        }))



# def delete_service_func(request, pk, pk_service):
#     user = User.objects.get(pk=pk)
#     service = ServiceModel.objects.get(pk=pk_service,user=user)
#     print(service.title)
#     service.delete()
#     return HttpResponseRedirect(reverse('dashboard_url', kwargs={
#             'pk': pk,

#         }))



class DeleteView(View):
    def get(self, request, pk, pk_service):
         user = User.objects.get(pk=pk)
         service = ServiceModel.objects.get(pk=pk_service,user=user)
         print(service.title)
         service.delete()
         return HttpResponseRedirect(reverse('dashboard_url', kwargs={
                    'pk': pk,

                }))
