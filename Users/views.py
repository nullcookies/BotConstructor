from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

from .models import Profile
from .forms import *


def base_view(request):
    context = {'title': 'Main - BotConstructor'}
    return render(request, 'Wrapper.html', context)


class ProfileView(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'show_bots_url'

    def get(self, request):
        current_user = Profile.objects.get(user=request.user)
        update_image_form = UpdateImageForm(instance=current_user)
        print(current_user.image)

        self.context.update({
            'title': 'Profile - BotCostructor',
            'current_user': current_user,
            'update_image_form': update_image_form
        })
        return render(request, 'Users/Profile.html', self.context)

    def post(self, request):
        current_user = Profile.objects.get(user=request.user)
        update_image_form = UpdateImageForm(
            request.POST, request.FILES, instance=current_user)

        if update_image_form.is_valid():
            update_image_form.save()
            return redirect('profile_url')

        self.context.update({
            'title': 'Profile - BotConstructor',
            'current_user': current_user,
            'update_image_form': update_image_form
        })
        return render(request, 'Users/Profile.html', self.context)


class UserRegistration(View):
    context = {}

    def get(self, request):
        register_form = UserRegistrationForm()

        self.context.update({
            'title': 'Registration - BotConstructor',
            'register_form': register_form
        })
        return render(request, 'Users/SignUp.html', self.context)

    def post(self, request):
        register_form = UserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            validate_url = 'https://www.google.com/recaptcha/api/siteverify'
            properties = {
                'secret': settings.GOOGLE_SECRET_KEY,
                'response': recaptcha_response
            }
            response = requests.get(validate_url, params=properties)

            if response.json()['success']:
                username = register_form.cleaned_data['username']
                first_name = register_form.cleaned_data['first_name']
                last_name = register_form.cleaned_data['last_name']
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password_some']
                password_confirm = register_form.cleaned_data[
                    'password_confirm'
                ]
                image = register_form.cleaned_data['image']
                about = register_form.cleaned_data['about']

                if password != password_confirm:
                    messages.error(request, 'Passwords do not match')
                else:
                    some_user = User.objects.create_user(
                        username=username, email=email, password=password,
                        first_name=first_name, last_name=last_name)
                    some_user.save()

                    some_user_profile = Profile.objects.create(
                        user=some_user, image=image, about=about)
                    some_user_profile.save()

                    new_user = authenticate(
                        username=username, password=password)
                    login(request, new_user)
                    return redirect('profile_url')
            else:
                messages.error(request, 'Sorry, you are the robot')

        self.context.update({
            'title': 'Registration - BotConstructor',
            'register_form': register_form
        })
        return render(request, 'Users/SignUp.html', self.context)


class UserAuthentication(View):
    context = {}

    def get(self, request):
        auth_form = UserAuthenticationForm()

        self.context.update({
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form
        })
        return render(request, 'Users/SignIn.html', self.context)

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
                    return redirect('profile_url')
                else:
                    messages.error(request, 'Password is incorrect')
            except ObjectDoesNotExist:
                messages.error(
                    request,
                    'Such user does not exits or you enter incorrect username')

        self.context.update({
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form
        })
        return render(request, 'Users/SignIn.html', self.context)


class UserLogout(View):
    def post(self, request):
        logout(request)
        return redirect('base_view_url')


class UpdateProfile(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'base_view_url'

    def get(self, request):
        update_form = UserRegistrationForm(instance=request.user)

        self.context.update({
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form
        })
        return render(request, 'Users/UpdateProfile.html', self.context)

    def post(self, request):
        update_form = UserRegistrationForm(request.POST, instance=request.user)
        current_user = User.objects.get(id=int(request.user.id))
        current_profile = Profile.objects.get(user=request.user)

        if update_form.is_valid():
            username = update_form.cleaned_data['username']
            first_name = update_form.cleaned_data['first_name']
            last_name = update_form.cleaned_data['last_name']
            email = update_form.cleaned_data['email']
            password = update_form.cleaned_data['password_some']
            about = update_form.cleaned_data['about']

            current_user.username = username
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            current_user.set_password(password)
            current_profile.about = about
            current_profile.save()
            current_user.save()

            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('profile_url')

        self.context.update({
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form
        })
        return render(request, 'Users/UpdateProfile.html', self.context)


# class UpdateImage(LoginRequiredMixin, View):
#     login_url = '/signIn/'
#     redirect_field_name = 'base_view_url'

#     def get(self, request):
#         current_profile = Profile.objects.get(user=request.user)
#         update_image_form = UpdateImageForm(instance=current_profile)

#         context = {
#             'title': 'Update Image - BotConstructor',
#             'update_image_form': update_image_form
#         }
#         return render(request, 'Users/UpdateImage.html', context)

#     def post(self, request):
#         current_profile = Profile.objects.get(user=request.user)
#         update_image_form = UpdateImageForm(
#             request.POST, request.FILES, instance=current_profile)

#         if update_image_form.is_valid():
#             update_image_form.save()
#             return redirect('profile_url')

#         context = {
#             'title': 'Update Image - BotConstructor',
#             'update_image_form': update_image_form
#         }
#         return render(request, 'Users/UpdateImage.html', context)


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
