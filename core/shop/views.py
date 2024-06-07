from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
import datetime
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .models import *


def main_view(request):
    # pic = Product.objects.all()
    # all_photos = []
    #
    # for p in pic:
    #     photo = Product.objects.filter(image=p)
    #     all_photos.extend(photo)
    #  'all_photos': all_photos
    context = {'categories': Category.objects.all(), 'products': Product.objects.all()}

    return render(request, 'shop/main.html', context)


def category_list_view(request):
    p = Paginator(Category.objects.all(), 4)
    context = {'cat': Category.objects.all()}

    return render(request, 'shop/categories.html', context)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        products = Product.objects.filter(category=self.object)
        context['products'] = products
        return context


def cart(request):
    my_cart = request.session.get('cart', [])

    if request.method == 'POST':
        cart_item_id = int(request.POST.get('cart_item'))

        if request.POST.get('add'):
            for i in my_cart:
                if i['product_id'] == cart_item_id:
                    i['quantity'] += 1
                    break
        elif request.POST.get('remove'):
            for i in my_cart:
                if i['product_id'] == cart_item_id:
                    i['quantity'] -= 1
                    if i['quantity'] == 0:
                        my_cart.remove(i)
                    break

        request.session['cart'] = my_cart
        request.session.modified = True
        return redirect('cart')

    my_cart_context = []
    total_price = 0

    for item in my_cart:
        product = get_object_or_404(Product, pk=item['product_id'])
        my_cart_item = {
            'product': product,
            'quantity': item['quantity'],
            'total': float(product.price * item['quantity'])
        }
        total_price += my_cart_item['total']
        my_cart_context.append(my_cart_item)

    processed_cart = Cart.objects.filter(user=request.user).order_by('-id')[:3]

    context = {
        'cart_items': my_cart_context,
        'total_price': total_price,
        'processed_cart': processed_cart
    }

    return render(request, 'shop/cart.html', context)


def add_to_cart(request, product_id):
    if not request.session.get('cart'):
        request.session['cart'] = []

    cart = request.session['cart']
    items = [i['product_id'] for i in cart]

    product = get_object_or_404(Product, pk=product_id)

    if product_id in items:
        for i in cart:
            if i['product_id'] == product_id:
                i['quantity'] += 1
                break
    else:
        cart_item = {
            "product_id": product_id,
            "quantity": 1
        }
        cart.append(cart_item)

    request.session.modified = True

    category_id = product.category.pk
    messages.add_message(request, messages.INFO, f"Product {product.name} added successfully")

    return redirect('category_detail', category_id)


def favorite(request):
    favorite_ids = request.session.get('favorites', [])
    favorite_products = Product.objects.filter(id__in=favorite_ids)
    context = {'favorite_products': favorite_products}

    return render(request, 'shop/favorites.html', context)


def add_to_favorite(request, product_id):
    if request.method == 'POST':
        request.session.modified = True
        favorites_list = request.session.get('favorites', [])
        if product_id not in favorites_list:
            favorites_list.append(product_id)
            request.session['favorites'] = favorites_list

        return redirect('favorites')


def contact(request):
    contact_inf = Contact.objects.all()
    context = {'contacts': contact_inf}

    return render(request, 'shop/contact.html', context)


def about(request):
    return render(request, 'shop/about.html')


# def checkout(request):
#     if request.method == 'POST':
#         cart_model = Cart.objects.create(user=request.user)
#         cart = request.session.get('cart', [])
#         for i in cart:
#             cart_item = CartItem.objects.create(product=Product.objects.get(pk=i['product']), count=i['quantity'])
#             cart_model.items.add(cart_item)
#         full_name = request.POST['full_name']
#         address = request.POST['address']
#         request.session['cart'] = []
#         request.session.modified = True
#         send_mail(
#             "Order details",
#             f"{full_name} get order to {address}",
#             "from@example.com",
#             ["to@example.com"],
#             fail_silently=False,
#         )
#         return redirect('checkout')
#
#     return render(request, 'shop/checkout.html')


# def latest_objects(request):
#     products = Product.objects.all().order_by('-created')[0]
#     context = {'latest_pr': products}
#
#     return render(request, 'shop/latest_products.html', context)
