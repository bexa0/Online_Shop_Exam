from django.urls import path
from .views import *

urlpatterns = [
    path('', main_view, name='start_page'),
    path('category/', category_list_view, name='categories'),
    path('category/detail/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', cart, name='cart'),
    path('add-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add-favorite/<int:product_id>/', add_to_favorite, name='add_to_favorite'),
    path('favorites/', favorite, name='favorites'),
    path('contacts/', contact, name='contact'),
    path('about/', about, name='about'),
    # path('checkout/', checkout, name='checkout'),
]
