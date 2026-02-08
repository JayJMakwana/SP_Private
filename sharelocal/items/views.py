from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        queryset = Item.objects.filter(status='Available').select_related('owner', 'category')

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.models import Category
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
