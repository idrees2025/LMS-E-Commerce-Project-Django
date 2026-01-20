from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from Base.utils import apply_sorting
from Shop.forms import ReviewForm
from django.db.models import Q,F,FloatField,ExpressionWrapper
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from Shop.models import Product,Category,Brands
# Create your views here.
class ProductDetailView(View):
    def get(self,request,pk,*args, **kwargs):
        products=Product.objects.get(pk=pk)
        reviews=products.reviews.all()
        form=ReviewForm()
        related=Product.objects.filter( Q(brand__name__icontains=products.brand.name)|
            Q(category__name__icontains=products.category.name))
        context={
            'product':products,
            'form':form,
            'reviews':reviews,
            'related':related
        }
        return render (request,'product_detail.html',context)
    
    def post(self,request,pk,*args, **kwargs):
        form=ReviewForm(request.POST)
        products=Product.objects.get(pk=pk)
        if form.is_valid():
            review=form.save(commit=False)
            review.user=request.user
            review.profile=request.user.profile
            review.product=products
            review.save()
            return redirect ('shop:product_detail',pk=pk)
        reviews=products.reviews.all()
        related=Product.objects.filter( Q(brand__name__icontains=products.brand.name)|
            Q(category__name__icontains=products.category.name))
        context={
            'product':products,
            'form':form,
            'reviews':reviews,
            'related':related
        }
        return render (request,'product_detail.html',context)

class FilterByPriceView(View):
    def get(self,request,*args, **kwargs):
        keyword=request.GET.get('keyword')
        product_list=Product.objects.filter(Q(category__name__icontains=keyword)|
            Q(brand__name__icontains=keyword))
        product_list = product_list.annotate(
        discounted_price=ExpressionWrapper(
        F('price') * (1 - F('percent_off') / 100),
        output_field=FloatField()
        )
        )
        max_price=request.GET.get('max_price')
        min_price=request.GET.get('min_price')
        if min_price:
            product_list=product_list.filter(discounted_price__gte=min_price)
        if max_price:
            product_list=product_list.filter(discounted_price__lte=max_price)
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        paginator=Paginator(product_list,9)
        page=request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context={'products':products,
                 'keyword':keyword,
                 'max_price':max_price,
                 'min_price':min_price,
                 'sort_by':current_sort
                 }
        return render(request,'products.html',context)
    
class CategoryProductListView(View):
    def get(self,request,slug,*args, **kwargs):
        category=get_object_or_404(Category,slug=slug)
        product_list=Product.objects.filter(category=category)
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        title=category.name
        paginator = Paginator(product_list,per_page=9)
        page = request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products = paginator.get_page(1)
        except EmptyPage:
            products=paginator.page(paginator.num_pages)
        context={'products':products,
            'title':title,
            'sort_by':current_sort
            }
        return render(request,'products.html',context)

class BrandProductListView(View):
    def get(self,request,slug,*args, **kwargs):
        brand = get_object_or_404(Brands, slug=slug)
        product_list = Product.objects.filter(brand=brand)
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        title = brand.name
        paginator = Paginator(product_list,per_page=9)
        page = request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products=paginator.get_page(1)
        except EmptyPage:
            products=paginator.get_page(paginator.num_pages)
        context={"products": products,
                "title": title,
                'sort_by':current_sort
                }
        return render(request, "products.html",context)

class TabBrandListView(View):
    def get(self,request,slug,*args, **kwargs):
        brand=get_object_or_404(Brands,slug=slug)
        product_list=Product.objects.filter(category__name='Tablet',brand=brand)
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        title = brand.name
        paginator = Paginator(product_list,per_page=9)
        page = request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products=paginator.get_page(1)
        except EmptyPage:
            products=paginator.get_page(paginator.num_pages)
        context={"products": products,
                "title":f'{title} Tablets',
                'sort_by':current_sort
                }
        return render(request, "products.html",context)

class MobileBrandListView(View):
    def get(self,request,slug,*args, **kwargs):
        brand=get_object_or_404(Brands,slug=slug)
        product_list=Product.objects.filter(category__name='Mobile Phone',brand=brand)
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        title = brand.name
        paginator = Paginator(product_list,per_page=9)
        page = request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products=paginator.get_page(1)
        except EmptyPage:
            products=paginator.get_page(paginator.num_pages)
            
        context={"products": products,
                "title":f'{title} mobiles ',
                'sort_by':current_sort
                }
        return render(request, "products.html",context)
    
class NewArivalView(View):
    def get(self,request,*args, **kwargs):
        product_list=Product.objects.order_by('-created_at')
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        paginator=Paginator(product_list,per_page=9)
        page = request.GET.get('page')
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products=paginator.get_page(1)
        except EmptyPage:
            products=paginator.get_page(paginator.num_pages)
        context={
            'title':'New Arrival',
            'products':products,
            'sort_by':current_sort
        }
        return render(request,'products.html',context)