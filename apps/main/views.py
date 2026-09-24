from django.shortcuts import render, get_object_or_404, redirect
from .models import HomeSlider, Category, Product, Comment, ContactRequest
from django.contrib import messages
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

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'main/shop.html', context)

def about_page(request):
    return render(request, 'main/about.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

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
            return redirect('login')

    comments = product.comments.all().order_by('-id')

    context = {
        'product': product,
        'comments': comments,
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
        # Ищем по name и description (так как в твоем Product используется name, а не title)
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'categories': categories,
        'products': products,
        'query': query,
    }
    return render(request, 'main/shop.html', context)


