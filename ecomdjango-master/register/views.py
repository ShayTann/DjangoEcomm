from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django import forms
from django.utils import timezone
from django.views.generic import DetailView,View,TemplateView, ListView
from django.conf import settings
from .forms import UserRegisterForm,UserEditForm,UserPwChange,ConactusForm
from django.conf.urls.static import static
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm,CheckoutForm,CouponForm,RefundForm,PaymentForm,UserLog,SubscribeForm
from django.contrib import messages
from .models import Item,OrderItem,Order,Address,Coupon,Profile,Payment,Contact,Subscriber
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q # new
import random
import string
import json
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
from urllib.request import urlopen
from django_countries import countries
import stripe
from django.core import serializers
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.mail import send_mail
# Create your views here.
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid
def register(response):
    if response.method == "POST":
        form = UserRegisterForm(response.POST)
        if form.is_valid():
            try:
                user = form.save()

            except :
                print("TO SKIP ERROR PAGE")
            finally :
                username = form.cleaned_data.get('username')
                pw = form.cleaned_data.get('password1')
                user =  authenticate(username= username , password = pw)
                login(response,user)
            return redirect('home')

    else:
        form = UserRegisterForm()

    return render(response,"auth/register.html",{"form":form})
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def home(response):

    Client_Country="Not found"

    ip = client_ip = response.META['REMOTE_ADDR'] # OR USE DEF GET_CLIENT_IP
    url = 'http://ip-api.com/php/'+ip  #TAKE OFF +ip for the test now we dont have a host so the ip will be always 127.0.0.1

    Client_Country = "Not found"
    ip = client_ip = response.META['REMOTE_ADDR'] # OR USE DEF GET_CLIENT_IP
    url = 'http://ip-api.com/php/'  #TAKE OFF +ip for the test now we dont have a host so the ip will be always 127.0.0.1

    rep = requests.get(url).content
    dataform = str(rep).strip("'<>() ").replace('\'', '\"')
    # data = json.loads(rep)
    for country in countries:
        if country[1] in dataform:
            print(country[1])
            Client_Country = country[1]

    if response.method == "POST":
        form = SubscribeForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubscribeForm()
    context = { 'items' : Item.objects.all(),
                'user' : response.user,
                'hot' : Item.objects.all().order_by('-views'),
                'form2':form,
                'client_country':Client_Country
    }

    return render(response,"layouts/homeContent.html",context)


class SearchResultsView(ListView):
    model = Item
    template_name = 'layouts/searchResult.html'

    def get_queryset(self): # new
        query = self.request.GET.get('query')
        object_list = Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list


def about_view(response):

    return render(response,"layouts/about.html")

def inbox(response):
    if response.user.is_superuser:
        if response.method=="POST":
            mails = Subscriber.objects.all()
            currentmsg = response.POST['message']
            send_mail('Contact Form',
            currentmsg,
            settings.EMAIL_HOST_USER,
            mails,
            fail_silently=False
            )

        context = {
            'messages' : Contact.objects.all(),
        }
        return render(response,"layouts/inbox.html",context)
    else :
        return redirect('contact')


def contact_view(response):

    if response.method == "POST":
        form =  ConactusForm(response.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except :
                pass
    else:

        form = ConactusForm()
    context = {
        'form':form
        }
    return render(response,"layouts/contact.html",context)


def thx_view(response):

    return render(response,"layouts/thankyou.html")



def category_view(response):
    context = {
                'items' : Item.objects.all(),
                'user' : response.user
    }
    return render(response,"layouts/category.html",context)

def shoesmanview(response):
    context = {'items' : Item.objects.filter(category="M"),
              'subcat' : Item.objects.filter(subcategory="Shoes")

    }
    return render(response,"layouts/category.html",context)
def menS_view(response,slug):
    try:
        subcat = get_object_or_404(Item, subcategory=slug).subcategory
        context= {'items' : Item.objects.filter(category="M",subcategory=str(subcat))}
        return render(response,"layouts/category.html",context)
    except :

        return render(response,"layouts/category.html")


def men_view(response):
    subcat = "ALL"
    context = {'items' : Item.objects.filter(category="M"),
              'subcat' : subcat

    }

    return render(response,"layouts/category.html",context)


def women_view(response):
    context = {'items' : Item.objects.filter(category="W"),

    }
    return render(response,"layouts/category.html",context)
def womenS_view(response,slug):
    try:
        subcat = get_object_or_404(Item, subcategory=slug).subcategory
        print(subcat)
        context= {'items' : Item.objects.filter(category="W",subcategory=str(subcat))}
        return render(response,"layouts/category.html",context)
    except :
        return render(response,"layouts/category.html")


def kids_view(response):
    context = {'items' : Item.objects.filter(category="K"),


    }
    return render(response,"layouts/category.html",context)

def kidsS_view(response,slug):
    try:
        subcat = get_object_or_404(Item, subcategory=slug).subcategory
        context= {'items' : Item.objects.filter(category="K",subcategory=str(subcat))}
        return render(response,"layouts/category.html",context)
    except :
        print("Erreur Pas d'item")
        return render(response,"layouts/category.html")


def login_view(request):
    if request.method == 'POST':
        form = UserLog(data =request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('..')
        else:
            messages.info(request, "Username or password incorrect")
    else:
        form = UserLog()



    return render(request,'auth/login.html',{'form':form})

def profile_view(request):
    if request.method == "POST":
        p_form = ProfileForm(request.POST, request.FILES , instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request,f'Your Account has been updated')
            return redirect('.')
    else :
        p_form = ProfileForm(instance=request.user.profile)
    args = { 'user' : request.user ,
             'p_form':p_form
    }
    return render (request,"profil/profilSettings.html",args)


def edit_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('../')

    else:
        form = UserEditForm(instance = request.user)
        args = { 'form' : form ,}
        return render(request,'register/edit.html',args)


def changePassword(request):
    if request.method =='POST':
        form=UserPwChange(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('../')
        else:
            return render(request,'auth/changepassword.html')
    else:
        form=UserPwChange(user = request.user)
        args = {'form':form}
        return render(request,'auth/changepassword.html',args)

def products_view(request):
    context = { 'items' : Item.objects.all()}
    return render(request,"layouts/shopSingle.html",context)

class ItemDetailView(DetailView):

    model = Item
    template_name = "layouts/shopSingle.html"

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    print(item.countries)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else :
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")

    else :
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("order_summary")

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)

            print("done")
            return redirect("order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order_summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order_summary", slug=slug)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'layouts/shop.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order_summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order_summary", slug=slug)
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,

                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,

                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")



                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.shipping_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.profile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a shipping address")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = Profile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")





def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                print(code)
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")
