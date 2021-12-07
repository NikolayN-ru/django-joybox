from django.urls import path
from .views import *

urlpatterns = [
	path('category/', category, name='category'),
	path('card/<int:id>', card, name='card'),
	path('', base, name='base'),
	path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
]