from django.shortcuts import render, get_object_or_404
from .models import HomeSlider, Category, Product

def home_page(request):
    photos = HomeSlider.objects.all()
    categories = Category.objects.all()
    context = {
        'photos': photos,
        'categories': categories,
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
    return render(request, 'main/product_detail.html', {'product': product})


