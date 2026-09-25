from django.shortcuts import render, get_object_or_404, redirect
from .models import HomeSlider, Category, Product, Comment, ContactRequest, Favorite, CartItem
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def home_page(request):
    photos = HomeSlider.objects.all()
    categories = Category.objects.all()

    all_products = Product.objects.all()

    context = {
        'photos': photos,
        'categories': categories,
        'recently_added_products': all_products.order_by('-id')[:4]
    }
    return render(request, 'main/index.html', context)


def shop_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    selected_category = None

    category_id = request.GET.get('category_id')

    if category_id:
        products = products.filter(category_id=category_id)
        selected_category = Category.objects.filter(id=category_id).first()

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'user_favorites': user_favorites,
    }
    return render(request, 'main/shop.html', context)


def about_page(request):
    return render(request, 'main/about.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart_item = None
    is_favorite = False

    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            if text:
                Comment.objects.create(
                    product=product,
                    user=request.user,
                    text=text
                )
                return redirect('product_detail', pk=pk)
        else:
            return redirect('users:home')

    comments = product.comments.all().order_by('-id')

    context = {
        'product': product,
        'comments': comments,
        'cart_item': cart_item,
        'is_favorite': is_favorite,
    }
    return render(request, 'main/product_detail.html', context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if first_name and email and message:
            ContactRequest.objects.create(
                first_name=first_name,
                lastname=lastname,
                email=email,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')

    return render(request, 'main/contact.html')


def search(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'categories': categories,
        'products': products,
        'query': query,
    }
    return render(request, 'main/shop.html', context)


def toggle_favorite(request, product_id):
    if not request.user.is_authenticated:
        return redirect('users:home')

    product = Product.objects.get(id=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user, product=product)

    return redirect('favorites_list')


def favorites_list(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    favorites = Favorite.objects.filter(user=request.user)

    ctx = {
        'favorites': favorites
    }
    return render(request, 'main/favorites.html', ctx)


def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('users:home')

    cart_items = CartItem.objects.filter(user=request.user)

    total_sum = 0
    total_quantity = 0
    for item in cart_items:
        clean_price = str(item.product.price).replace(',', '').replace('$', '').strip()
        total_sum += float(clean_price) * item.quantity
        total_quantity += item.quantity

    context = {
        'cart_items': cart_items,
        'total_sum': round(total_sum, 2),
        'total_quantity': total_quantity,
    }
    return render(request, 'main/cart.html', context)


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('users:home')

    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=1)

    return redirect('cart_detail')


def update_cart_quantity(request, item_id, action):
    if not request.user.is_authenticated:
        return redirect('users:home')

    cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
    if cart_item:
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('users:home')

    cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
    if cart_item:
        cart_item.delete()

    return redirect('cart_detail')


