from django.db import models
from accounts.models import Profile
from django.conf import settings
from django.utils.text import slugify

class Brands(models.Model):
    name=models.CharField(max_length=222,null=True,blank=True)
    image=models.ImageField(upload_to='photo/',null=True,blank=True)
    slug=models.SlugField(unique=True,null=True,blank=True)

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name=models.CharField(max_length=222)
    image=models.ImageField(upload_to='photo/',null=True,blank=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    brand=models.ForeignKey(Brands,on_delete=models.CASCADE,related_name='products')
    title=models.CharField(max_length=222)
    price=models.DecimalField(max_digits=20, decimal_places=2)
    percent_off=models.PositiveIntegerField()
    stock=models.IntegerField()
    varrianty=models.CharField(max_length=222)
    created_at=models.DateTimeField(auto_now_add=True)

    def main_image(self):
        first_image=self.images.first()
        if first_image:
            return first_image.image.url
        return None
    
    def discounted_price(self):
        if self.percent_off > 0:
            discount_amount = (self.percent_off / 100) * float(self.price)
            return round(float(self.price) - discount_amount, 2)
        return float(self.price)

    def __str__(self):
        return self.title

class Productimage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='products/')

class ProductFeautures(models.Model):
    product=models.ForeignKey(Product,related_name='feautures',on_delete=models.CASCADE)
    title=models.CharField(max_length=222)
    value=models.TextField()

class ProductDescription(models.Model):
    product=models.ForeignKey(Product,related_name='descriptions',on_delete=models.CASCADE)
    title=models.CharField(max_length=222)
    des=models.TextField()
    image=models.ImageField(upload_to='photo/')

class Review(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.IntegerField(choices=((i,i)for i in range(1,6)))
    review=models.TextField()
    title=models.CharField(max_length=222)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "profile"],
                name="unique_review_per_user_per_product"   
            )
        ]

    def __str__(self):
        return f'{self.product} - {self.profile.user}'