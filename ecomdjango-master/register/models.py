from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from autoslug import AutoSlugField
# Create your models here.
CATEGORY_CHOICES = ( ('MEN','WOMEN'),
('WOMEN','WOMEN'),
('KIDS','KIDS'),
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
    one_click_purchasing = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'




class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)







class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    belongsToCat = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)







class Item(models.Model):
    title = models.CharField(max_length=100)
    sex = models.CharField(blank=True,null=True,max_length=50)
    price = models.FloatField()
    description = models.TextField(default="Hey")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_pics')
    slug = AutoSlugField(populate_from='title')
    discount_price=models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
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
