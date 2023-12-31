from django.shortcuts import render, get_object_or_404

from .models import ProductProxy, Category


def products_view(request):
    context = {}
    products = ProductProxy.objects.all()
    context['products'] = products  
    return render(request, 'shop/products.html', context)

def product_detail_view(request, slug):
    context = {}
    product = get_object_or_404(ProductProxy, slug=slug)
    context['product'] = product
    return render(request, 'shop/product_detail.html', context)

def categories_list(request, slug):
    context = {}
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context.update({'category': category, 'products': products})
    return render(request, 'shop/categories_list.html', context)