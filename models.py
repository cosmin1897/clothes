# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ShopMagCart(models.Model):
    status = models.CharField(max_length=50)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_mag_cart'


class ShopMagCartitem(models.Model):
    cart = models.ForeignKey(ShopMagCart, models.DO_NOTHING)
    item = models.ForeignKey('ShopMagItem', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shop_mag_cartitem'


class ShopMagCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'shop_mag_category'


class ShopMagContactrequest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25)
    email = models.CharField(max_length=254)
    title = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        managed = False
        db_table = 'shop_mag_contactrequest'


class ShopMagItem(models.Model):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    price = models.FloatField()
    label = models.CharField(max_length=2)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(ShopMagCategory, models.DO_NOTHING)
    stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shop_mag_item'


class ShopMagProductsize(models.Model):
    size = models.CharField(max_length=20)
    stock = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    product = models.ForeignKey(ShopMagItem, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_mag_productsize'


class ShopMagShippingaddress(models.Model):
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField()
    customer = models.ForeignKey('ShopMagCustomer', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('ShopMagOrder', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_mag_shippingaddress'
