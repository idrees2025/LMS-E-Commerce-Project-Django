from Shop.models import Brands,Category,Product
from django.db.models import Q,Count
from Cart.models import CartItem

def header_and_footer_data(request):
    if request.user.is_authenticated:
        return{
            'nav_brands' : Brands.objects.all(),
            'nav_categories' : Category.objects.all(),
            'footer_p' : Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count'),
            'pop_iphone' : Product.objects.filter(
                Q(category__name__icontains='mobile'),
                Q(brand__name__icontains='apple')).
                annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
            'pop_samsung' : Product.objects.filter(
                Q(category__name__icontains='mobile'),
                Q(brand__name__icontains='samsung')).
                annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
          'pop_sony' : Product.objects.filter(
                Q(category__name__icontains='mobile'),
                Q(brand__name__icontains='sony')).
                annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
            'pop_microsoft' : Product.objects.filter(
                Q(category__name__icontains='mobile'),
                Q(brand__name__icontains='microsoft')).
                annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
            'nav_cart' : CartItem.objects.filter(user=request.user)[:3]
            } 
    return{   
       'nav_brands' : Brands.objects.all(),
        'nav_categories' : Category.objects.all(),
        'footer_p' : Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count'),
        'pop_iphone' : Product.objects.filter(
            Q(category__name__icontains='mobile'),
            Q(brand__name__icontains='apple')).
            annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
        'pop_samsung' : Product.objects.filter(
            Q(category__name__icontains='mobile'),
            Q(brand__name__icontains='samsung')).
            annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
        'pop_sony' : Product.objects.filter(
            Q(category__name__icontains='mobile'),
            Q(brand__name__icontains='sony')).
            annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
        'pop_microsoft' : Product.objects.filter(
            Q(category__name__icontains='mobile'),
            Q(brand__name__icontains='microsoft')).
            annotate(review_count=Count('reviews')).order_by('-review_count')[:6],
    }
  