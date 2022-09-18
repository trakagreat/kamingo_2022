import os.path



import requests

import random
from django.db import models
from django.db.models.signals import post_save
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator , MinLengthValidator
from django.contrib.auth.models import User
from django.utils.text import slugify

from kamingo.settings import STATIC_URL
from .static import serviceapp


# file renaming function ----------------
def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    randomstr = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('service_photos', randomstr)


# models ----------------------------

class Address(models.Model):
    address_line1 = models.CharField(max_length=100, null=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='City')
    pin_code = models.CharField(max_length=6, null=True, validators=[MinLengthValidator(6)])
    locality = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.address_line1}, {self.pin_code}, {self.city}"
    
    def pin_to_address(self , pin):
        address = requests.get('https://api.postalpincode.in/pincode/' + str(pin))
        return address.json()
        



    def save(self, *args, **kwargs):
        try:
            self.locality = self.pin_to_address(self.pin_code)[0]['PostOffice'][0]['Name']
        except:
            pass
        super(Address, self).save(*args, **kwargs)
        
      
        
        


class CategoryModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ServiceModel(models.Model):
    # image = models.FileField(upload_to=path_and_rename, null=True , blank=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, related_name='category', null=True)
    cost = models.IntegerField()
    service_provider_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10, null=True, validators=[MinLengthValidator(10)])
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='address', null=True)
    slug = models.SlugField(unique=True, db_index=True, null=True, blank=True)
    description = models.CharField(max_length=600, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user',null=True)
    # address2 = AddressField(null=True, blank=True , on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_rating(self):
        total = sum(int(review['rating']) for review in self.reviews.values())
        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0
    
    def get_image(self):
        try:
            image = self.images.first().image.url
        except:
            image = None
        return image

    # get all images of a service
    def get_images(self):
        images = []
        for image in self.images.all():
            images.append(image.image.url)
        if len(images) == 0:
            images = None
            return images
        else:
            return images

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(ServiceModel, self).save(*args, **kwargs)

    def slugify(self):
        self.slug = slugify(self.title)


class ImageModel(models.Model):
    image = models.FileField(upload_to=path_and_rename, null=True , blank=True)
    service = models.ForeignKey(ServiceModel, on_delete=models.SET_NULL, related_name='images', null=True, blank=True)

    def __str__(self):
        return f"{self.image}"



class ReviewModel(models.Model):
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE, related_name='reviews', null=True)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    content = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.rating} {self.user} {self.service}"

    class Meta:
        ordering = ['-date_added']





# image compression code

def image_compressor(sender, **kwargs):
    if kwargs["created"]:
        with Image.open(kwargs["instance"].image.path) as photo:
            photo.save(kwargs["instance"].image.path, optimize=False, quality=100)


post_save.connect(image_compressor, sender=ImageModel)


