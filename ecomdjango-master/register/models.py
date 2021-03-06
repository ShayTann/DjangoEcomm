from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from autoslug import AutoSlugField
from multiselectfield import MultiSelectField
from django_countries import countries
# Create your models here.
CATEGORY_CHOICES = (('M','MEN'),
('W','WOMEN'),
('K','KIDS'),
)
subCat = (
    ('Shirt','Shirt'),
    ('Shoes','Shoes'),
    ('Jack','Jack'),
    ('Jeans','Jeans'),
    ('Hoodies','Hoodies'),
    ('Accesories','Accesories'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    sex = models.CharField(blank=True,null=True,max_length=50)
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)


    one_click_purchasing = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'




class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(default="Item Description")
    views = models.IntegerField(default="0")
    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        )
    subcategory = models.CharField(
        max_length = 20,
        choices = subCat,
        blank = True,
        null=True,
        )
    image = models.ImageField(upload_to='item_pics')
    slug = AutoSlugField(populate_from='title')
    discount_price=models.FloatField(blank=True,null=True)
    countries = MultiSelectField(choices=countries,
                                 max_choices=10,
                                 max_length=20,default="Morocco")
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        self.views=self.views+1
        self.save()
        return reverse("products",kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):

        return reverse("add-to-cart",kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart",kwargs={
            'slug':self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
class Contact(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    numero = models.CharField(max_length=50,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
class Subscriber(models.Model):
    email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return f'{self.email}'

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = Profile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
