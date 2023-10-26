from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import CartItem, Product, Cart


def home(request):
    product = Product.objects.all()
    context = {
        'product': product,
    }
    return render(
        request,
        template_name='app/home.html',
        context=context
    )


@login_required(login_url='/login/')
def all_product_add_user(request):
    customer_cart_items = CartItem.objects.filter(cart_id=request.user.id)
    if customer_cart_items:
        total_price = _get_cart_total(request)

        context = {
            'total_price': total_price,
            'customer_cart_items': customer_cart_items,
        }

        return render(
            request,
            context=context,
            template_name='app/cart_view.html'
        )

    return render(request, 'app/cart_view.html')


def about(request):
    return render(request, 'app/about.html')


def _get_cart_total(request):
    cart = Cart.objects.get(id=request.user.id)

    cart_items = cart.cartitem_set.all()

    total_price = 0

    for cart_item in cart_items:
        product_price = cart_item.product.price
        quantity = cart_item.quantity
        item_total = product_price * quantity
        total_price += item_total

    return total_price


def add_product_to_cart(request, product_id):
    # Получите пользователя, который вошел в систему
    user = request.user

    # Получите товар, который вы хотите добавить в корзину
    product = get_object_or_404(Product, id=product_id)

    # Получите корзину пользователя или создайте ее, если она еще не существует
    cart, created = Cart.objects.get_or_create(customer=user)

    # Проверьте, существует ли товар уже в корзине, и увеличьте количество, если да
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')


def delete_product_from_cart(request, product_id):
    user = request.user

    product = get_object_or_404(Product, id=product_id)

    cart = Cart.objects.get(customer=user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('cart')
