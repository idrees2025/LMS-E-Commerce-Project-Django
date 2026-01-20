from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import stripe,datetime,json
from django.utils.crypto import get_random_string
from django.db import transaction
from django.db.models import F
from Cart.forms import ShippingAddressForm
from django.conf import settings
from Cart.models import CartItem,Order,OrderItem,ShippingAddress
from Shop.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# Create views here..

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(login_required(login_url='account:login'),name='dispatch')    
class AddtocartView(View):
    def get(self,request,pk,*args, **kwargs):
        product=get_object_or_404(Product,pk=pk)
        try:
            c_items=CartItem.objects.get(user=request.user,product=product)
            c_items.quantity +=1
        except CartItem.DoesNotExist:
            c_items=CartItem.objects.create(user=request.user,product=product)
        c_items.save()
        return redirect("cart:checkout_cart")

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class RemovefromcartView(View):
    def get(self,request,pk,*args, **kwargs):
        c_item=get_object_or_404(CartItem,pk=pk,user=request.user)
        c_item.delete()
        return redirect("cart:checkout_cart")

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class IncreaseQuantityQiew(View):
    def get(self,request,pk,*args, **kwargs):
        c_item=get_object_or_404(CartItem,pk=pk,user=request.user)
        c_item.quantity += 1
        c_item.save()
        return redirect('cart:checkout_cart')
    
@method_decorator(login_required(login_url='account:login'),name='dispatch')
class DecreseQuantityView(View):
    def get(self,request,pk,*args, **kwargs):
        c_item=get_object_or_404(CartItem,pk=pk,user=request.user)
        if c_item.quantity > 1:
           c_item.quantity -= 1
        c_item.save()
        return redirect ('cart:checkout_cart')
    
@method_decorator(login_required(login_url='account:login'),name='dispatch')
class CheckoutCartView(View):
    def get(self,request,*args, **kwargs):
        c_items=CartItem.objects.filter(user=request.user)
        total=sum(item.total_price() for item in c_items)
        context={'c_items':c_items,'total':total}
        return render(request, "checkout_cart.html",context)
    
    def post(self,request,*args,**kwargs):
        has_address = ShippingAddress.objects.filter(user=request.user).exists()
        if has_address:
            return redirect('cart:checkout_payment')
        else:
            return redirect('cart:checkout_info')
        
@method_decorator(login_required(login_url='account:login'),name='dispatch')
class CheckoutInfoView(View):
    def get(self,request,*args,**kwargs):
        form=ShippingAddressForm()
        return render(request, 'checkout_info.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            address.user=request.user
            address.save()
            return redirect('cart:checkout_payment')
        return render(request, 'checkout_info.html',{'form':form})

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class UpdateShippingAddressView(View):
    def get(self,request,pk,*args,**kwargs):
        data=ShippingAddress.objects.get(pk=pk)
        form=ShippingAddressForm(instance=data)
        return render(request,'checkout_info.html',{'form':form})

    def post(self,request,pk,*args, **kwargs):
        data=ShippingAddress.objects.get(pk=pk)
        form=ShippingAddressForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('account:account')
        return render(request,'checkout_info.html',{'form':form})

@login_required(login_url='account:login')
def checkout_payment_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart:checkout_cart')
    subtotal = sum(item.total_price() for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        order_number=get_random_string(12).upper(),
        subtotal=subtotal,
        total=subtotal,
    )
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.discounted_price(),
            quantity=item.quantity,
        )
    return render(request,'checkout_payment.html',
        {'order':order,
         'total':subtotal,
        'STRIPE_PUBLISHABLE_KEY':settings.STRIPE_PUBLIC_KEY})

@require_POST
@login_required(login_url='account:login')
def create_payment_intent(request):
    data = json.loads(request.body)
    user=request.user
    order = Order.objects.get(id=data["order_id"], user=user)
    intent = stripe.PaymentIntent.create(
        amount=int(order.subtotal*100),
        currency="pkr",
        automatic_payment_methods={"enabled": True},
        customer=user.stripe_customer_id,
    )
    order.stripe_payment_intent_id = intent.id
    order.save()

    return JsonResponse({
        "clientSecret": intent.client_secret
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        intent_id = intent["id"]
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(
                    stripe_payment_intent_id=intent_id
                )
                if order.is_paid:
                    return HttpResponse(status=200)
                for item in order.items.select_related("product"):
                    if item.product.stock < item.quantity:
                        raise ValueError("Insufficient stock")
                    item.product.stock = F('stock') - item.quantity
                    item.product.save(update_fields=['stock'])
                order.is_paid = True
                order.status = "on the way"
                order.paid_at = datetime.datetime.now()
                order.save()
                CartItem.objects.filter(user=order.user).delete()
        except Order.DoesNotExist:
            print("Order not found")
    return HttpResponse(status=200)

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_stripe_refund(payment_intent_id, amount=None):
    try:
        refund_params = {
            'payment_intent': payment_intent_id,
        }
        if amount is not None:
            refund_params['amount'] = amount
        refund = stripe.Refund.create(**refund_params)
        return refund

    except stripe.StripeError as e:
        print(f"Stripe error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

@login_required(login_url='account:login')
def refund_payment_view(request, order_id):
    order=Order.objects.select_for_update().get(id=order_id)
    if request.method == 'POST':
        payment_intent_id = order.stripe_payment_intent_id
        refund_result = process_stripe_refund(payment_intent_id)
        if "error" not in refund_result:
            order.status = 'refund'
            order.is_paid=False
            for items in order.items.select_related('product'):
                items.product.stock = F('stock') + items.quantity
                items.product.save(update_fields=['stock'])
            order.save()
            return redirect('cart:return_items')
        else:
            print("something went wrong")
    return render(request, 'confirm_refund.html', {'order': order})

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class ReturnItemsView(View):
    def get(self,request,*args, **kwargs):
        orders=Order.objects.filter(user=request.user,status='refund')
        return render(request,'return_items.html',{'orders':orders})

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class TrackShipmentView(View):
    def get(self,request,*args, **kwargs):
        orders=Order.objects.filter(user=request.user,is_paid=True,status='on the way').order_by('-paid_at')
        return render(request,'track_shipment.html',{'orders':orders})

@login_required(login_url='account:login')
def checkout_complete_view(request,order_id):
    orders=Order.objects.filter(id=order_id,user=request.user,is_paid=True)
    if request.method == 'POST':
        return redirect('cart:track_shipment')
    return render (request,'checkout_complete.html',{'orders':orders})

@method_decorator(login_required(login_url='account:login'),name='dispatch')
class OrderHistoryView(View):
    def get(self,request,*args, **kwargs):
        orders=Order.objects.filter(user=request.user,is_paid=True,status='delivered').order_by('-paid_at')
        return render(request,'order_history.html',{'orders':orders})