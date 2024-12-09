from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductSearchForm

def products_view(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.filter(stock__gte=1).order_by('category__name', 'title')

    if form.is_valid() and form.cleaned_data['query']:
        products = products.filter(title__icontains=form.cleaned_data['query'])

    return render(request, 'store/products.html', {'products': products, 'form': form})


def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product.html', {'product': product})


def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_view')
    else:
        form = CategoryForm()
    return render(request, 'store/category_add.html', {'form': form})


def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.id:
                product.save()
            return redirect('product_view', id=product.id)
    else:
        form = ProductForm()
    return render(request, 'store/product_add.html', {'form': form})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def product_edit_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_view', id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_edit.html', {'form': form, 'product': product})


def product_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('products_view')
    return render(request, 'store/product_confirm_delete.html', {'product': product})
