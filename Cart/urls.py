from django.urls import path
from Cart import views

app_name='cart'

urlpatterns = [
    path("checkout/", views.CheckoutCartView.as_view(), name="checkout_cart"),
    path('remove/<int:pk>/',views.RemovefromcartView.as_view(),name='remove_cart'),
    path('add/<int:pk>/',views.AddtocartView.as_view(),name='add_cart'),
    path('checkout-info/',views.CheckoutInfoView.as_view(),name='checkout_info'),
    path('checkout-payemnt/',views.checkout_payment_view,name='checkout_payment'),
    path('checkout-complete/<int:order_id>/',views.checkout_complete_view,name='checkout_complete'),
    path('increse/<int:pk>/',views.IncreaseQuantityQiew.as_view(),name='increase_quantity'),
    path('decrease/<int:pk>/',views.DecreseQuantityView.as_view(),name='decrease_quantity'),
    path('orders/',views.OrderHistoryView.as_view(),name='order_history'),
    path('updateshippingadddress/<int:pk>/',views.UpdateShippingAddressView.as_view(),name='update_shipping_address'),
    path('returns/items/',views.ReturnItemsView.as_view(),name='return_items'),
    path("track/shipment/",views.TrackShipmentView.as_view(), name="track_shipment"),
    path('create-payment-intent/',views.create_payment_intent,name='create_payment_intent'),
    path('stripe/webhook/',views.stripe_webhook),
    path('refund/<int:order_id>/',views.refund_payment_view,name='refund'),
]