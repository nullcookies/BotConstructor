from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

from .forms import UserRegistrationForm, UserAuthenticationForm, UpdateImageForm
from .models import Profile


def base_view(request):
    return render(request, 'Wrapper.html', context={'title': 'Main - BotConstructor'})


class UserRegistration(View):
    def get(self, request):
        register_form = UserRegistrationForm()

        context = {
            'title': 'Registration - BotConstructor',
            'register_form': register_form
        }
        return render(request, 'Users/SignUp.html', context)

    def post(self, request):
        register_form = UserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            validate_url = 'https://www.google.com/recaptcha/api/siteverify'
            properties = {
                'secret': settings.GOOGLE_SECRET_KEY,
                'response': recaptcha_response
            }
            url = requests.get(validate_url, params=properties)

            if url.json()['success']:
                username = register_form.cleaned_data['username']
                first_name = register_form.cleaned_data['first_name']
                last_name = register_form.cleaned_data['last_name']
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password_some']
                image = register_form.cleaned_data['image']

                some_user = User.objects.create_user(
                    username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                some_user.save()

                some_user_profile = Profile.objects.create(
                    user=some_user, image=image)
                some_user_profile.save()

                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                return redirect('base_view_url')
            else:
                messages.error(request, 'Sorry, you are the robot')

        context = {
            'title': 'Registration - BotConstructor',
            'register_form': register_form
        }
        return render(request, 'Users/SignUp.html', context)


class UserAuthentication(View):
    def get(self, request):
        auth_form = UserAuthenticationForm()

        context = {
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form
        }
        return render(request, 'Users/SignIn.html', context)

    def post(self, request):
        auth_form = UserAuthenticationForm(request.POST)

        if auth_form.is_valid():
            password = auth_form.cleaned_data['password']
            username = auth_form.cleaned_data['username']

            try:
                current_user = User.objects.get(username=username)
                if current_user.check_password(password):
                    new_user = authenticate(
                        username=username, password=password)
                    login(request, new_user)
                    return redirect('base_view_url')
                else:
                    messages.error(request, 'Password is incorrect')
            except ObjectDoesNotExist:
                messages.error(
                    request, 'Such user does not exits or you enter incorrect username')

        context = {
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form
        }
        return render(request, 'Users/SignIn.html', context)


class UserLogout(View):
    def post(self, request):
        logout(request)
        return redirect('base_view_url')


class UpdateProfile(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'base_view_url'

    def get(self, request):
        update_form = UserRegistrationForm(instance=request.user)

        context = {
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form
        }
        return render(request, 'Users/UpdateProfile.html', context)

    def post(self, request):
        update_form = UserRegistrationForm(request.POST, instance=request.user)
        current_user = User.objects.get(id=int(request.user.id))

        if update_form.is_valid():
            username = update_form.cleaned_data['username']
            first_name = update_form.cleaned_data['first_name']
            last_name = update_form.cleaned_data['last_name']
            email = update_form.cleaned_data['email']
            password = update_form.cleaned_data['password_some']

            current_user.username = username
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            current_user.set_password(password)
            current_user.save()

            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('base_view_url')

        context = {
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form
        }
        return render(request, 'Users/UpdateProfile.html', context)


class UpdateImage(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'base_view_url'

    def get(self, request):
        current_profile = Profile.objects.get(user=request.user)
        update_image_form = UpdateImageForm(instance=current_profile)

        context = {
            'title': 'Update Image - BotConstructor',
            'update_image_form': update_image_form
        }
        return render(request, 'Users/UpdateImage.html', context)

    def post(self, request):
        current_profile = Profile.objects.get(user=request.user)
        update_image_form = UpdateImageForm(
            request.POST, request.FILES, instance=current_profile)

        if update_image_form.is_valid():
            update_image_form.save()
            return redirect('base_view_url')

        context = {
            'title': 'Update Image - BotConstructor',
            'update_image_form': update_image_form
        }
        return render(request, 'Users/UpdateImage.html', context)


class UserDelete(View):
    def get(self, request):
        context = {
            'title': 'Delete User - BotConstructor',
        }
        return render(request, 'Users/DeleteUser.html', context)

    def post(self, request):
        user = User.objects.get(id=int(request.user.id))
        user.delete()
        return redirect('base_view_url')
