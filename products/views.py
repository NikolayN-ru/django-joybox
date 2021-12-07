from django.shortcuts import render
from django.views.generic import DetailView
from .models import Smartphone, Notebook


def base(request):
    return render(request, 'index.html', {})


def category(request):
    return render(request, 'category.html', {})


def card(request, id):
    return render(request, 'card.html', {})


class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'card.html'
    slug_url_kwarg = 'slug'
