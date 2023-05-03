from django.urls import path

from . import views

app_name = 'shop_mag'

urlpatterns = [
    path('', views.ListaProduse.as_view(), name='home'),
    path('order-item/', views.CartDetailView.as_view(), name='order_item'),
    path("category/<int:pk>", views.CategoryDetails.as_view(), name="category"),
    path('product-details/<int:pk>/', views.ItemDetailView.as_view(), name='product_details'),
    path('cart/', views.open_cart_view, name='cart'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('contact/', views.ContactRequestCreateView.as_view(), name='contact'),
    # path('login/', views.MyLoginView.as_view(), name='my_login_view'),
    # path('logout/', LogoutView.as_view(), {'next_page': reverse_lazy('my_login_view')}, name='my_logout_view'),
    path('add-product-to-cart/', views.add_product_to_cart, name='add_product_to_cart'),
    path('update-profile/<int:pk>', views.UserUpdateView.as_view(), name='update_profile'),
]
