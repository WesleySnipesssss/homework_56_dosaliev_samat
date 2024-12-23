from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, ProductSearchForm

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
