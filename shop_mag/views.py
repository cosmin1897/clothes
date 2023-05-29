from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, RedirectView

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


class CartDetailView(DetailView):
    model = Cart
    context_object_name = "order_i2tem"
    template_name = "order.html"


class CategoryDetails(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_details.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('shop_mag:home')


# class HomeView(TemplateView):
#     template_name = 'home.html'


class SearchListView(ListView):
    model = Item
    template_name = 'search_results.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        return Item.objects.filter(name__icontains=self.request.GET.get('q'))


def get_open_cart(request):
    open_cart = Cart.objects.filter(user=request.user, status='open').first()
    if open_cart is None:
        open_cart = Cart.objects.create(user=request.user, status='open')
    return open_cart


@login_required(login_url=reverse_lazy('login'))
def open_cart_view(request):
    cart: Cart = get_open_cart(request)
    print(f'cart={cart}')
    return render(request, 'order.html', {'cart': cart})


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_profile.html'


@login_required
def add_product_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity', 1)

        open_cart = get_open_cart(request)

        existing_cart_item = CartItem.objects.filter(item_id=item_id, cart=open_cart).first()
        if existing_cart_item is None:
            existing_cart_item = CartItem.objects.create(item_id=item_id, cart=open_cart, quantity=quantity)
        else:
            existing_cart_item.quantity += int(quantity)
            existing_cart_item.save()
        if int(existing_cart_item.quantity) <= 0:
            existing_cart_item.delete()
    return redirect(request.META['HTTP_REFERER'])


class ContactRequestCreateView(CreateView):
    model = ContactRequest
    form_class = ContactRequestForm
    template_name = 'contact.html'
    success_url = reverse_lazy('shop_mag:home')


class CustomLogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return CustomLogoutView.as_view()(request, *args, **kwargs)


def checkout_view(request):
    cart = get_open_cart(request)
    cart.status = 'closed'
    cart.save()
    return redirect(request.META['HTTP_REFERER'])


