from django.urls import path
from Base import views

app_name='base'

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('faq/',views.faq_view,name='faq'),
    path('about-us/',views.about_view,name='about'),
    path('contact-us/',views.ContactUsView.as_view(),name='contact'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('index-fixed/',views.IndexFixedView.as_view(),name='index_fixed_header'),
    path("index-inversed/",views.IndexInversedView.as_view(), name="index_inverse_header")
]
