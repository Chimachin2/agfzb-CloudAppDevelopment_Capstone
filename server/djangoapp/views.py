from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request, get_single_dealers
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:index")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/4faf8dbd-d6b2-4192-af16-f96ff1a3f43f/dealership-package/get-dealership/"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        parameters={dealer_id}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/4faf8dbd-d6b2-4192-af16-f96ff1a3f43f/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, kwargs=parameters)
        dealership = get_single_dealers(dealer_id=dealer_id)
        context["review_list"] = reviews
        context["dealership"] = dealership["dealer"]
        context['dealer_id'] = dealer_id
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        context = {}
        if request.method == 'GET':
            cars = CarModel.objects.filter(Dealerid=dealer_id)
            context["cars"] = cars
            context["dealer_id"] = dealer_id
            context["dealership"] = get_single_dealers(dealer_id=dealer_id)["dealer"]
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            car_id = int(request.POST["car"])
            car = CarModel.objects.get(pk=car_id)
            username = request.user
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST['review']
            review["id"] = random.randint(0,9999)
            review["name"] = username.first_name + " " + username.last_name
            review["purchase"] = False
            if 'purchasecheck' in request.POST:
                if request.POST['purchasecheck'] == 'on':
                    review["purchase"] = True
            review["purchase_date"] = request.POST['purchase_date']
            review["car_make"] = car.make.Name
            review["car_model"] = car.Name
            review["car_year"] = int(car.Year.strftime("%Y"))

            url = "https://us-south.functions.appdomain.cloud/api/v1/web/4faf8dbd-d6b2-4192-af16-f96ff1a3f43f/dealership-package/post-review"
            json_payload = {}
            json_payload["review"] = review
            post_request(url, json_payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')