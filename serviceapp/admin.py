from django.contrib import admin

from .models import ImageModel, ServiceModel, CategoryModel , ReviewModel, Address

# Register your models here.

admin.site.register(ServiceModel)
admin.site.register(CategoryModel)
admin.site.register(ReviewModel)
admin.site.register(Address)
admin.site.register(ImageModel)

