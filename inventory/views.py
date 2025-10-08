from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from .models import SoldProduct, Product
from .forms import ProductForm, SellForm


class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                name__icontains=query
            )
        return queryset

class ProductAddView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_add.html'

    def get_success_url(self):
        return reverse_lazy('product-list')

class ProductSellView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = SellForm(initial={'sold_price': product.price})
        return render(request, 'inventory/product_sell.html', {'product': product, 'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = SellForm(request.POST)
        if form.is_valid() and product.quantity > 0:
            sold_price = form.cleaned_data['sold_price']
            product.quantity -= 1
            product.save()

            SoldProduct.objects.create(
                product=product,
                product_name=product.name,  # Shu qo‘shiladi
                sold_price=sold_price
            )
            return redirect('sold-product-list')
        return render(request, 'inventory/product_sell.html', {'product': product, 'form': form})

class SoldProductListView(ListView):
    model = SoldProduct
    template_name = 'inventory/sold_product_list.html'
    context_object_name = 'sold_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        all_sold = SoldProduct.objects.all()
        context['sold_products'] = all_sold

        # Umumiy statistika
        total_cost = sum([sp.product.cost_price * sp.quantity if sp.product else 0 for sp in all_sold])
        total_revenue = sum([sp.total_price for sp in all_sold])
        context['total_count'] = all_sold.count()
        context['total_cost'] = total_cost
        context['total_revenue'] = total_revenue
        context['total_profit'] = total_revenue - total_cost

        # Kundalik statistika
        today = now.date()
        daily_sold = all_sold.filter(sold_at__date=today)
        daily_cost = sum([sp.product.cost_price * sp.quantity if sp.product else 0 for sp in daily_sold])
        daily_revenue = sum([sp.total_price for sp in daily_sold])
        context['daily_count'] = daily_sold.count()
        context['daily_cost'] = daily_cost
        context['daily_revenue'] = daily_revenue
        context['daily_profit'] = daily_revenue - daily_cost

        # Haftalik statistika
        week_start = now - timedelta(days=7)
        weekly_sold = all_sold.filter(sold_at__gte=week_start)
        weekly_cost = sum([sp.product.cost_price * sp.quantity if sp.product else 0 for sp in weekly_sold])
        weekly_revenue = sum([sp.total_price for sp in weekly_sold])
        context['weekly_count'] = weekly_sold.count()
        context['weekly_cost'] = weekly_cost
        context['weekly_revenue'] = weekly_revenue
        context['weekly_profit'] = weekly_revenue - weekly_cost

        # Oylik statistika
        month_start = now - timedelta(days=30)
        monthly_sold = all_sold.filter(sold_at__gte=month_start)
        monthly_cost = sum([sp.product.cost_price * sp.quantity if sp.product else 0 for sp in monthly_sold])
        monthly_revenue = sum([sp.total_price for sp in monthly_sold])
        context['monthly_count'] = monthly_sold.count()
        context['monthly_cost'] = monthly_cost
        context['monthly_revenue'] = monthly_revenue
        context['monthly_profit'] = monthly_revenue - monthly_cost

        return context



def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product-list')
