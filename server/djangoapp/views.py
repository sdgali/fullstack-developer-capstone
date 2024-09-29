# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        data = {"userName": username}
    else:
        data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
    except KeyError:
        return JsonResponse({"error": "Invalid data provided"}, status=400)

    username_exist = False
    email_exist = False
    
    # Check if username exists
    if User.objects.filter(username=username).exists():
        username_exist = True

    # Check if email exists
    if User.objects.filter(email=email).exists():
        email_exist = True

    if username_exist:
        data = {"userName": username, "error": "Username already exists"}
        return JsonResponse(data, status=409)  # Conflict error
    
    if email_exist:
        data = {"email": email, "error": "Email already registered"}
        return JsonResponse(data, status=409)

    # If it is a new user
    if not username_exist and not email_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        # Login the user and return success response
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data, status=201)  # Created

    # If there was an error in the process
    return JsonResponse({"error": "Registration failed"}, status=400)



def get_cars(request):
    # Get the count of CarMake objects
    count = CarMake.objects.filter().count()
    print(count)
    
    # If no CarMake exists, populate the database
    if count == 0:
        initiate()
    
    # Fetch CarModel objects with their related CarMake using 'car_make'
    car_models = CarModel.objects.select_related('car_make')
    
    # Create a list of car model names with their respective car makes
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    
    # Return the car models in a JSON response
    return JsonResponse({"CarModels": cars})
    

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
