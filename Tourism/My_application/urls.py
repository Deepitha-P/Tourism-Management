
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from My_application.views import (
    home_view, signup_view, login_view, logout_view,
    dashboard, browse_packages, bookings, reviews,
    features_view, pricing_view, faqs_view, about_view,
    book_package,remove_booking_view, payment_page
   , download_receipt,payment_success_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('features/', features_view, name='features'),
    path('pricing/', pricing_view, name='pricing'),
    path('faqs/', faqs_view, name='faqs'),
    path('about/', about_view, name='about'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('browse_packages/', browse_packages, name='browse_packages'),
    path('bookings/', bookings, name='bookings'),
    path('reviews/', reviews, name='reviews'),
    path('book_package/<int:package_id>/', book_package, name='book_package'),
    path('bookings/', bookings, name='bookings'),
    path('remove_booking/<int:booking_id>/', remove_booking_view, name='remove_booking'),
    path('download_receipt/<int:booking_id>/', download_receipt, name='download_receipt'),
    path('payment/<int:booking_id>/', payment_page, name='payment'),
    path('payment-success/<int:booking_id>/', payment_success_page, name='payment_success'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
