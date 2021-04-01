from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from PaysafeTest.settings import PAYSAFE_PUBLIC_KEY, PAYSAFE_PRIVATE_KEY
from payments.forms import SignUpForm, PaymentForm
from payments.helper import HelperPaySafe


def home(request):
    customer_token = None
    if request.method == 'POST':
        request.POST._mutable = True

        form = PaymentForm(request.POST)

        if form.is_valid():
            paysafe_user_id = HelperPaySafe.get_or_create_paysafe_customer_profile(request.user)
            customer_token = HelperPaySafe.get_single_user_customer_token(paysafe_user_id)
            form.data['is_submit_clicked'] = 1

            profile_instance = request.user.profile
            profile_instance.address = form.cleaned_data.get('address')
            profile_instance.mobile = form.cleaned_data.get('mobile')
            profile_instance.city = form.cleaned_data.get('city')
            profile_instance.pincode = form.cleaned_data.get('pincode')
            profile_instance.save()
    else:
        django_user_instance = request.user
        if django_user_instance.is_authenticated:
            init_data = {
                'mobile': django_user_instance.profile.mobile,
                'address': django_user_instance.profile.address,
                'city': django_user_instance.profile.city,
                'pincode': django_user_instance.profile.pincode,
                'paysafe_user_id': django_user_instance.profile.paysafe_user_id,
                'is_submit_clicked': 0,
            }
        else:
            init_data = {}

        form = PaymentForm(initial=init_data)
    return render(request=request, template_name="home.html", context={'form': form,
                                                                       'paysafe_public_key': PAYSAFE_PUBLIC_KEY,
                                                                       'private_public_key': PAYSAFE_PRIVATE_KEY,
                                                                       'customer_token': customer_token})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request=request, template_name='signup.html', context={'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")
