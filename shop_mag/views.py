from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView

from .forms import ContactRequestForm, UserForm, UserUpdateForm
from .models import *


# Create your views here.


# def home(request):
#     items = Item.objects.all()
#     return render(request, "home.html", items)

class RedirectClassMix(UserPassesTestMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseRedirect(reverse_lazy('homepage'))
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        pass


class ListaProduse(ListView):
    model = Item
    context_object_name = 'lista_produse'
    template_name = 'home.html'


class ItemDetailView(DeleteView):
    model = Item
    context_object_name = "item"
    template_name = "product_detailts.html"


class Cart(DetailView):
    model = OrderItem, Order
    context_object_name = "order_item"
    template_name = "order.html"


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('shop_mag:home')


class CategoryDetails(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_details.html'


class ContactRequestCreateView(CreateView):
    model = ContactRequest
    form_class = ContactRequestForm
    template_name = 'contact.html'
    success_url = reverse_lazy('home')


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_profile.html'


def order(request):
    # print(request.META)
    context = {}
    return render(request, "order.html", context)


# def cart(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer


def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)


def get_open_cart(request):
    open_cart = Order.objects.get_or_create(user=request.user)
    # open_cart = Order.objects.filter().first()
    # if open_cart is None:
    print(open_cart)
    #     open_cart = Order.objects.create(user=request.user, ordered_date=None)
    return open_cart


@login_required()
def open_cart_view(request):
    cart: Cart = get_open_cart(request)
    print(f'cart={cart}')
    return render(request, 'order.html', {'cart': cart})


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = get_open_cart(request)

    order = order_qs[0]
    order_item, created = OrderItem.objects.get_or_create(item=item, order=order)
    # check if the order item is in the order
    if order.items.filter(item__slug=item.slug).first() is not None:
        order_item.quantity += 1
        order_item.save()
        # messages.info(request, "This item quantity was updated.")
        return redirect("shop_mag:order")
    else:
        order.items.add(order_item)
        # messages.info(request, "This item was added to your cart.")
        return redirect("shop_mag:order")
    # else:
    #     ordered_date = timezone.now()
    #     order = Order.objects.create(
    #         user=request.user, ordered_date=ordered_date)
    #     order.items.add(order_item)
    #     # messages.info(request, "This item was added to your cart.")
    #     return redirect("shop_mag:order")


def register(request):
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


