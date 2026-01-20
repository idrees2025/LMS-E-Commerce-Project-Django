from django.shortcuts import render,redirect
from django.views import View
from Base.models import ContactUs
from django.db.models import Count,Q,Avg
from Base.utils import apply_sorting
from Shop.models import Product,Category,Brands
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
# Create your views here.

def faq_view(request):
    return render(request,'faq.html')

def about_view(request):
    return render(request,'about.html')

class ContactUsView(View):
    def get(self,request,*args, **kwargs):
        return render(request,'contact_us.html')

    def post(self,request,*args, **kwargs):
        contact=ContactUs.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
        return redirect('base:home')

class IndexView(View):
    def get(self,request,*args, **kwargs):
        trending_list=Product.objects.annotate(review_avg=Avg('reviews')).order_by('-review_avg')[:10]
        paginator=Paginator(trending_list,6)
        page=request.GET.get('page')
        try:
            trendings = paginator.page(page)
        except PageNotAnInteger:
            trendings = paginator.page(1)
        except EmptyPage:
            trendings = paginator.page(paginator.num_pages)
        mobile_b=Product.objects.filter(category__name='Mobile Phone').values_list('brand__name',flat=True).distinct()
        tablet_bnon=Product.objects.filter(category__name='Tablet').values_list('brand__name',flat=True).distinct()
        tab_cat=Category.objects.filter(name='Tablet')
        mobile_cat=Category.objects.filter(name='Mobile Phone')
        slider1=Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')
        slider2=Product.objects.filter(category__name='TV').order_by('-created_at')
        slider3=Product.objects.filter(category__name='Tablet').order_by('-created_at')
        mobiles=Product.objects.filter(category__name__icontains='mobile').order_by('-created_at')
        watch=Product.objects.filter(category__name__icontains='gadget').order_by('-created_at')
        tv=Product.objects.filter(category__name__icontains='tv').order_by('-created_at')
        laptops=Product.objects.filter(category__name__icontains='laptop').order_by('-created_at')
        t=Product.objects.filter(category__name__icontains='tablet').order_by('-created_at')

        context={
                'mobile_b':mobile_b,'tab_b':tablet_bnon,
                'tab_cat':tab_cat,'mobile_cat':mobile_cat,
                'trendings':trendings,'mobiles':mobiles,
                'laptops':laptops,'tvs':tv,'watches':watch,
                'tablets':t,'slider1':slider1,'slider2':slider2,
                'slider3':slider3
                }
        return render(request,'index.html',context)
    
class SearchView(View):
    def get(self,request,*args, **kwargs):
        search=request.GET['search']
        product_list=Product.objects.filter(Q(title__icontains=search)| 
            Q(category__name__icontains=search))
        product_list,current_sort=apply_sorting(product_list,request,default='created_at')
        paginator=Paginator(product_list,9)
        page=request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context={
            'products':products,
            'search':search,
            'sort_by':current_sort
        }
        return render(request,'search.html',context)
    
class IndexFixedView(View):
    def get(self,request,*args, **kwargs):
        trending_list=Product.objects.annotate(review_avg=Avg('reviews')).order_by('-review_avg')[:10]
        paginator=Paginator(trending_list,6)
        page=request.GET.get('page')
        try:
            trendings = paginator.page(page)
        except PageNotAnInteger:
            trendings = paginator.page(1)
        except EmptyPage:
            trendings = paginator.page(paginator.num_pages)
        mobile_b=Product.objects.filter(category__name='Mobile Phone').values_list('brand__name',flat=True).distinct()
        tablet_bnon=Product.objects.filter(category__name='Tablet').values_list('brand__name',flat=True).distinct()
        tab_cat=Category.objects.filter(name='Tablet')
        mobile_cat=Category.objects.filter(name='Mobile Phone')
        slider1=Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')
        slider2=Product.objects.filter(category__name='TV').order_by('-created_at')
        slider3=Product.objects.filter(category__name='Tablet').order_by('-created_at')
        mobiles=Product.objects.filter(category__name__icontains='mobile').order_by('-created_at')
        watch=Product.objects.filter(category__name__icontains='gadget').order_by('-created_at')
        tv=Product.objects.filter(category__name__icontains='tv').order_by('-created_at')
        laptops=Product.objects.filter(category__name__icontains='laptop').order_by('-created_at')
        t=Product.objects.filter(category__name__icontains='tablet').order_by('-created_at')

        context={
                'mobile_b':mobile_b,'tab_b':tablet_bnon,
                'tab_cat':tab_cat,'mobile_cat':mobile_cat,
                'trendings':trendings,'mobiles':mobiles,
                'laptops':laptops,'tvs':tv,'watches':watch,
                'tablets':t,'slider1':slider1,'slider2':slider2,
                'slider3':slider3
                }
        return render(request,'index_fixed_header.html',context)
    
class IndexInversedView(View):
    def get(self,request,*args, **kwargs):
        trending_list=Product.objects.annotate(review_avg=Avg('reviews')).order_by('-review_avg')[:10]
        paginator=Paginator(trending_list,6)
        page=request.GET.get('page')
        try:
            trendings = paginator.page(page)
        except PageNotAnInteger:
            trendings = paginator.page(1)
        except EmptyPage:
            trendings = paginator.page(paginator.num_pages)
        mobile_b=Product.objects.filter(category__name='Mobile Phone').values_list('brand__name',flat=True).distinct()
        tablet_bnon=Product.objects.filter(category__name='Tablet').values_list('brand__name',flat=True).distinct()
        tab_cat=Category.objects.filter(name='Tablet')
        mobile_cat=Category.objects.filter(name='Mobile Phone')
        slider1=Product.objects.annotate(review_count=Count('reviews')).order_by('-review_count')
        slider2=Product.objects.filter(category__name='TV').order_by('-created_at')
        slider3=Product.objects.filter(category__name='Tablet').order_by('-created_at')
        mobiles=Product.objects.filter(category__name__icontains='mobile').order_by('-created_at')
        watch=Product.objects.filter(category__name__icontains='gadget').order_by('-created_at')
        tv=Product.objects.filter(category__name__icontains='tv').order_by('-created_at')
        laptops=Product.objects.filter(category__name__icontains='laptop').order_by('-created_at')
        t=Product.objects.filter(category__name__icontains='tablet').order_by('-created_at')

        context={
                'mobile_b':mobile_b,'tab_b':tablet_bnon,
                'tab_cat':tab_cat,'mobile_cat':mobile_cat,
                'trendings':trendings,'mobiles':mobiles,
                'laptops':laptops,'tvs':tv,'watches':watch,
                'tablets':t,'slider1':slider1,'slider2':slider2,
                'slider3':slider3
                }
        return render(request,'index_inverse_header.html',context)