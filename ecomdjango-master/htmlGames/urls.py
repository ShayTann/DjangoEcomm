"""htmlGames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from register import views as v
from django.contrib.auth import login,views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',v.register,name ='register'),
    path('search/', v.SearchResultsView.as_view(), name='search_results'),
    path('about/',v.about_view,name ='about'),
    path('contact/',v.contact_view,name ='contact'),
    path('category/',v.category_view,name ='category'),
    path('men/',v.men_view,name ='men'),
    path('men/<slug>',v.menS_view,name ='menS'),
    path('wom/',v.women_view,name ='wom'),
    path('wom/<slug>',v.womenS_view,name ='womenS'),
    path('kids/',v.kids_view,name ='kids'),
    path('kids/<slug>',v.kidsS_view,name ='kidsS'),
    path('thanks/',v.thx_view,name ='thanks'),
    path('inbox/',v.inbox,name ='inbox'),

    path('',v.home,name='home'),


    url(r'^login/$',v.login_view,name='login'),
    url(r'^profile/$',v.profile_view,name='profile'),
    url(r'^profile/edit/$',v.edit_view,name='edit'),
    url(r'^profile/changepassword',v.changePassword,name='changepassword'),
    path('', include('django.contrib.auth.urls')),
    path('products/<slug>/',v.itemV,name ='products'),
    path('add-to-cart/<slug>/',v.add_to_cart,name ='add-to-cart'),
    path('remove-from-cart/<slug>/',v.remove_from_cart,name ='remove-from-cart'),
    path('order-summary/',v.OrderSummaryView.as_view(),name ='order_summary'),
    path('remove-item-from-cart/<slug>/', v.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('checkout/', v.CheckoutView.as_view(), name='checkout'),
    path('add-coupon/',v.AddCouponView.as_view(), name='add-coupon'),
    path('payment/<payment_option>/', v.PaymentView.as_view(), name='payment'),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
