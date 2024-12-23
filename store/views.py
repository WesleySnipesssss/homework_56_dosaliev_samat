
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Product, Category, CartItem
from .forms import ProductForm, ProductSearchForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'store/category_add.html'
    success_url = reverse_lazy('products')

class ProductListView(ListView):
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gte=1).order_by('category__name', 'title')
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSearchForm(self.request.GET or None)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_add.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_view', kwargs={'pk': self.object.pk})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_edit.html'

    def get_success_url(self):
        return reverse_lazy('product_view', kwargs={'pk': self.object.pk})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('products_view')

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    if product.stock == 0 or quantity <= 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('products_view')))
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)
    else:
        cart_item.quantity = min(quantity, product.stock)
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('products_view')))

def cart_view(request):
    cart_items = CartItem.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('cart_view')))

def remove_one_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('cart_view')))
