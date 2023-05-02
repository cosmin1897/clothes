from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from clothes import settings

# Create your models here.


# SALES_CHOICES = (
#     ('P', 'primary'),
#     ('S', 'secondary'),
#     ('D', 'danger'),
# )

COLORS = (
    ('WHITE', 'WHITE'),
    ('RED', 'RED'),
    ('BLUE', 'BLUE'),
    ('BLACK', 'BLACK'),
    ('YELLOW', 'YELLOW'),
    ('GREEN', 'GREEN'),
)

LABEL_CHOICES = (
    ("XL", "ExtraLarge"),
    ("L", "Large"),
    ("M", "Medium"),
    ("S", "Small"),
)

gender = (
    ('Men', 'Men'),
    ('Women', 'Women')
)


class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Category(models.Model):
    name = models.CharField(max_length=100)


    def items(self):
        return Item.objects.filter(category=self)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, blank=False)
    color = models.CharField(choices=COLORS, max_length=50)
    gender = models.CharField(choices=gender, max_length=10)
    description = models.TextField(null=True)
    stock = models.IntegerField(default=10)
    photo = models.ImageField(null=True, max_length=255, upload_to="static/")
    slug = models.SlugField(auto_created=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop_mag:product_details", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("shop_mag:add-to-cart", kwargs={'slug': self.slug})

    @property
    def get_image(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url


class Order(models.Model):  # CART
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def order_items(self):
        return OrderItem.objects.filter(order=self)

    @property
    def get_cart_total_price(self):
        orderitems = OrderItem.objects.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = OrderItem.objects.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def cart_items(self):
        return OrderItem.objects.filter(order=self)





class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_total_item_price(self):
        total = self.item.price * self.quantity
        return total

    def get_final_price(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_total.price()
        return total



class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()
    title = models.CharField(max_length=255)
    message = models.TextField()


@receiver(post_save, sender=ContactRequest)
def contact_request_save(sender, instance, created, *args, **kwargs):
    if created:
        send_mail('New contact request', f'Contact requested: {instance}', settings.EMAIL_HOST_USER,
                  [settings.EMAIL_HOST_USER])

