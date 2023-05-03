from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from clothes import settings

# Create your models here.


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

    @property
    def get_image(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url


class Cart(models.Model):
    STATUS = (
        ("open", "Open"),
        ("closed", "Closed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS)

    def cart_items(self):
        return CartItem.objects.filter(cart=self)

    def __str__(self):
        return f'{self.status} cart of {self.user.username}'

    def total(self):
        return sum([c.total() for c in self.cart_items()])


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} X {self.item} in {self.cart}'

    def total(self):
        return self.item.price * self.quantity


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
