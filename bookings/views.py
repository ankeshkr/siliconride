from django.shortcuts import render, redirect
from .models import PickupPoint, DestinationPoint, Traveller, Booking
from .forms import BookingForm
from .forms import RegisterForm
from django.http import JsonResponse

from django.shortcuts import render
from .models import PickupPoint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import CustomUser
import random

def home(request):
    pickup_points = PickupPoint.objects.all()

    if request.method == "POST":
        origin_id = request.POST.get('pickup_point')
        destination_id = request.POST.get('destination')

        # Ensure both origin and destination are selected
        if not origin_id or not destination_id:
            return render(request, 'bookings/home.html', {
                'pickup_points': pickup_points,
                'error': "Please select both pickup and destination points."
            })

        # Store the selections in session
        request.session['origin_id'] = origin_id
        request.session['destination_id'] = destination_id

        # Redirect to the select_seat page
        return redirect('select_seat')

    return render(request, 'bookings/home.html', {'pickup_points': pickup_points})

@login_required
def select_seat(request):
    origin_id = request.session.get('origin_id')
    destination_id = request.session.get('destination_id')

    # Get all travelers linked to the selected pickup point
    travellers = Traveller.objects.filter(pickup_point_id=origin_id)

    travellers_data = []
    for traveller in travellers:
        # Get booked seats for this traveler
        bookings = Booking.objects.filter(traveller=traveller)
        booked_seats = bookings.values_list('seat_number', flat=True)

        # Calculate available seats
        available_seats = [
            seat for seat in range(1, traveller.total_seats + 1)
            if seat not in booked_seats
        ]

        # Append traveler data with available seats
        travellers_data.append({
            'traveller': traveller,
            'available_seats': available_seats,
        })

    if request.method == "POST":
        seat_number = int(request.POST.get('seat_number'))
        traveller_id = int(request.POST.get('traveller_id'))
        traveller = Traveller.objects.get(id=traveller_id)

        Booking.objects.create(
            user=request.user,
            origin_id=origin_id,
            destination_id=destination_id,
            traveller=traveller,
            seat_number=seat_number
        )
        return redirect('confirmation')

    return render(request, 'bookings/select_seat.html', {'travellers_data': travellers_data})
# def select_seat(request):
#     print("inside select_seat function")
#     origin_id = request.session.get('origin_id')
#     destination_id = request.session.get('destination_id')
#     traveller = Traveller.objects.first()  # Simplified: assume a single traveller for now

#     if not traveller:
#         return render(request, 'bookings/select_seat.html', {
#             'error': "No traveller is available. Please contact the administrator."
#         })

#     bookings = Booking.objects.filter(traveller=traveller)
#     booked_seats = bookings.values_list('seat_number', flat=True)
#     available_seats = [
#         seat for seat in range(1, traveller.total_seats + 1)
#         if seat not in booked_seats
#     ]

#     if request.method == "POST":
#         seat_number = int(request.POST.get('seat_number'))
#         Booking.objects.create(
#             user=request.user,
#             origin_id=origin_id,
#             destination_id=destination_id,
#             traveller=traveller,
#             seat_number=seat_number
#         )
#         return redirect('confirmation')

#     return render(request, 'bookings/select_seat.html', {'available_seats': available_seats})


def confirmation(request):
    return render(request, 'bookings/confirmation.html', {'message': "Your seat has been successfully booked!"})

def get_destinations(request):
    pickup_point_id = request.GET.get('pickup_point')
    destinations = DestinationPoint.objects.filter(origin__id=pickup_point_id)
    destination_list = list(destinations.values('id', 'name'))  # Serialize data
    return JsonResponse(destination_list, safe=False)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = RegisterForm()
    return render(request, 'bookings/register.html', {'form': form})

otp_cache = {}  # Temporary in-memory cache for OTPs (use a proper database or external service in production)

def send_otp(mobile):
    otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
    otp_cache[mobile] = otp
    print(f"OTP for {mobile}: {otp}")  # Replace with actual SMS sending logic

def otp_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')

        if otp:  # OTP verification
            cached_otp = otp_cache.get(mobile)
            if cached_otp and str(cached_otp) == otp:
                user = CustomUser.objects.filter(mobile=mobile).first()
                if user:
                    login(request, user)
                    del otp_cache[mobile]  # Clear OTP after successful login
                    return redirect('home')
                else:
                    return render(request, 'bookings/otp_login.html', {'error': 'User not found'})
            else:
                return render(request, 'bookings/otp_login.html', {'error': 'Invalid OTP'})
        else:  # OTP generation
            user = CustomUser.objects.filter(mobile=mobile).first()
            if user:
                send_otp(mobile)
                return render(request, 'bookings/otp_login.html', {'mobile': mobile, 'otp_sent': True})
            else:
                return render(request, 'bookings/otp_login.html', {'error': 'User not found'})
    return render(request, 'bookings/otp_login.html')
