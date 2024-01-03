from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress


@login_required(login_url="account:login")
def shipping(request):
    context = {}
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect("account:dashboard")

    context["form"] = form
    return render(request, "payment/shipping.html", context)


def checkout(request):
    context = {}
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            context["shipping_address"] = shipping_address
            return render(request, "payment/checkout.html", context)
    return render(request, "payment/checkout.html")


def complite_order(request):
    if request.POST.get("action") == "payment":
        name = request.POST.get("name")
        email = request.POST.get("email")
        street_address = request.POST.get("street_address")
        apartment_address = request.POST.get("apartment_address")
        country = request.POST.get("country")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": name,
                "email": email,
                "street_address": street_address,
                "apartment_address": apartment_address,
                "country": country,
                "zip": zip_code,
                "city": city,
            },
        )

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user, shipping_address=shipping_address, amount=total_price
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                    user=request.user,
                )
        else:
            order = Order.objects.create(
                shipping_address=shipping_address, amount=total_price
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                )
        return JsonResponse({"success": True})

def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "payment/payment-success.html")


def payment_fail(request):
    return render(request, "payment/payment-fail.html")
