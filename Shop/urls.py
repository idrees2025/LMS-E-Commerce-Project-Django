from django.urls import path
from Shop import views

app_name='shop'

urlpatterns = [
    path('detail/<int:pk>/',views.ProductDetailView.as_view(),name='product_detail'),
    path("filtering/",views.FilterByPriceView.as_view(), name="filtering"),
    path("mobile-brand/<slug:slug>/",views.MobileBrandListView.as_view(), name="mobile_brand"),
    path('tablet-brand/<slug:slug>/',views.TabBrandListView.as_view(),name='tablet_brand'),
    path("brand/<slug:slug>/",views.BrandProductListView.as_view(), name="brand_products"),
    path("category/<slug:slug>/",views.CategoryProductListView.as_view(), name="category_products"),
    path('new-arrival/',views.NewArivalView.as_view(),name='new_arrival'),
]
