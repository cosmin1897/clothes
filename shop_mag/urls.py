from django.urls import path
from . import views


app_name = 'shop_mag'

urlpatterns = [
    path('home/', views.ListaProduse.as_view(), name='home'),
    path('order-item/', views.Cart.as_view(), name='order_item'),
    path('order/', views.order, name='order'),
    path("category/<int:pk>", views.CategoryDetails.as_view(), name="category"),
    path('product-details/<slug>/', views.ItemDetailView.as_view(), name='product_details'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.ContactRequestCreateView.as_view(), name='contact'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('update-profile/<int:pk>', views.UserUpdateView.as_view(), name='update_profile'),
]
