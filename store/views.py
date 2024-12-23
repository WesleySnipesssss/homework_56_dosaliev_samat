
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Product, Category, CartItem, Order, OrderProduct, Cart
from .forms import ProductForm, ProductSearchForm, OrderForm
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


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart_view')


def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart = request.session.get('cart', {})
        cart_items = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            cart_items.append({'product': product, 'quantity': quantity})

    total_price = sum(item['product'].price * item['quantity'] for item in cart_items)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_name = request.user.username if request.user.is_authenticated else 'Guest'
            order.save()

            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    product=cart_item['product'],
                    quantity=cart_item['quantity']
                )

            if request.user.is_authenticated:
                cart_items.delete()
            else:
                request.session['cart'] = {}

            return redirect('products_view')

    else:
        form = OrderForm()

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })


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
