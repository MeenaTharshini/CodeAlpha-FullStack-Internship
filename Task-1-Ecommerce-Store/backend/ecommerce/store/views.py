from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist, Order
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count() if request.user.is_authenticated else 0

    return render(request, 'store/product_list.html', {
        'products': products,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1

    request.session['cart'] = cart

    messages.success(request, f"{product.name} added to cart 🛒")
    return redirect('product_list')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'store/cart.html', context)
@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('product_list')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {
        'wishlist_items': wishlist_items
    })

def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')

def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

#####Order placement
@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total_price = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * qty

    Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # Clear cart after order
    request.session['cart'] = {}

    return render(request, 'store/order_success.html', {
        'total_price': total_price
    })
##########MY ORDE?R???S

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})