from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,  BookingForm , ReviewForm
from .models import Destination, Package, Booking , Review
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from fpdf import FPDF




def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Extracting form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Creating a new user
            User.objects.create_user(username=username, email=email, password=password)

            # Redirect to login page after successful signup
            return redirect('login')
        else:
            # Re-render the form with errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def browse_packages(request):
    packages = Package.objects.all()
    destinations = Destination.objects.all()

    # Filtering based on request parameters
    destination_id = request.GET.get('destination')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if destination_id:
        packages = packages.filter(destination_id=destination_id)
    if price_min:
        packages = packages.filter(price__gte=price_min)
    if price_max:
        packages = packages.filter(price__lte=price_max)

    context = {
        'packages': packages,
        'destinations': destinations
    }
    return render(request, 'browse_packages.html', context)

@login_required
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.end_date = booking.start_date + timedelta(days=package.number_of_days)
            booking.total_persons = form.cleaned_data['total_persons']
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_package.html', {'package': package, 'form': form})


@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def remove_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('bookings')
    return render(request, 'remove_booking.html', {'booking': booking})

@login_required
def reviews(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    reviews = Review.objects.all()
    packages = Package.objects.all()

    context = {
        'reviews': reviews,
        'packages': packages,
        'form': form,
    }

    return render(request, 'reviews.html', context)


def features_view(request):
    return render(request, 'features.html')

def pricing_view(request):
    return render(request, 'pricing.html')

def faqs_view(request):
    return render(request, 'faqs.html')

def about_view(request):
    return render(request, 'about.html')


# Payment Page
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        # You might want to process the payment here
        
        # After processing payment, redirect to a success page
        return redirect('payment_success', booking_id=booking.id)
    
    total_amount = booking.package.price * booking.total_persons
    return render(request, 'payment.html', {'booking': booking, 'total_amount': total_amount})


def payment_success_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment_success.html', {'booking_id': booking.id})




def download_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    pdf = FPDF()
    pdf.add_page()

    # Add content to PDF
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Booking ID: {booking_id}", ln=True)
    pdf.cell(200, 10, txt=f"Package: {booking.package.name}", ln=True)
    pdf.cell(200, 10, txt=f"Start Date: {booking.start_date}", ln=True)
    pdf.cell(200, 10, txt=f"End Date: {booking.end_date}", ln=True)
    pdf.cell(200, 10, txt=f"Total Persons: {booking.total_persons}", ln=True)
    pdf.cell(200, 10, txt=f"Total Price: ${booking.total_persons * booking.package.price}", ln=True)

    # Save the PDF to a BytesIO object
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=receipt_{booking_id}.pdf'
    return response