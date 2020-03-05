from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import EmailMessage

import requests

from .models import Profile
from .forms import *
from .tokens import account_activation_token


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
                about = register_form.cleaned_data['about']

                some_user = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
                some_user.is_active = False
                some_user.save()

                some_user_profile = Profile.objects.create(
                    user=some_user, about=about)
                some_user_profile.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('ActiveEmail.html', {
                    'user': some_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(some_user.pk)),
                    'token': account_activation_token.make_token(some_user),
                    'request': request
                })
                to_email = register_form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                messages.error(
                    request,
                    'Now, a message will come to your mail'
                )

                return redirect('base_view_url')
            else:
                messages.error(request, 'Sorry, you are the robot')

        self.context.update({
            'title': 'Registration - BotConstructor',
            'register_form': register_form
        })
        return render(request, 'Users/SignUp.html', self.context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile_url')
    else:
        return HttpResponse('Activation link is invalid!')


class UserAuthentication(View):
    context = {}

    def get(self, request):
        auth_form = UserAuthenticationForm()

        if 'tries_captcha' not in request.session.keys():
            request.session['tries_captcha'] = 0

        if 'tries_captcha' in request.session.keys() \
                and request.session['tries_captcha'] > 1:
            is_captcha = True
        else:
            is_captcha = False

        self.context.update({
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form,
            'is_captcha': is_captcha
        })
        return render(request, 'Users/SignIn.html', self.context)

    def post(self, request):
        auth_form = UserAuthenticationForm(request.POST)

        if 'tries_captcha' not in request.session.keys():
            request.session['tries_captcha'] = 0

        if 'tries_captcha' in request.session.keys() and \
                request.session['tries_captcha'] > 1:
            is_captcha = True
        else:
            is_captcha = False

        if auth_form.is_valid():
            password = auth_form.cleaned_data['password']
            username = auth_form.cleaned_data['username']

            if 'tries_captcha' in request.session.keys() and \
                    request.session['tries_captcha'] > 1:
                recaptcha_response = request.POST.get(
                    'g-recaptcha-response')
                validate_url = ('https://www.google.com/recaptcha/'
                                'api/siteverify')
                properties = {
                    'secret': settings.GOOGLE_SECRET_KEY,
                    'response': recaptcha_response
                }
                response = requests.get(validate_url, params=properties)

                if response.json()['success']:
                    try:
                        current_user = User.objects.get(username=username)
                        if current_user.check_password(password):
                            new_user = authenticate(
                                username=username, password=password)

                            try:
                                login(request, new_user)
                            except AttributeError:
                                messages.error(
                                    request,
                                    'Firstly, you must confirm your email'
                                )

                            return redirect('profile_url')
                        else:
                            request.session['tries_captcha'] += 1
                            messages.error(request, 'Password is incorrect')

                    except ObjectDoesNotExist:
                        messages.error(
                            request,
                            'Such user does not exits or '
                            'you enter incorrect username'
                        )
                else:
                    messages.error(request, 'Sorry, you are the robot')
            else:
                try:
                    current_user = User.objects.get(username=username)
                    if current_user.check_password(password):
                        new_user = authenticate(
                            username=username, password=password)
                        try:
                            login(request, new_user)
                        except AttributeError:
                            messages.error(
                                request,
                                'Firstly, you must confirm your email'
                            )

                        return redirect('profile_url')
                    else:
                        request.session['tries_captcha'] += 1
                        messages.error(request, 'Password is incorrect')

                except ObjectDoesNotExist:
                    messages.error(
                        request,
                        'Such user does not exits or '
                        'you enter incorrect username'
                    )

        self.context.update({
            'title': 'Authentication - BotConstructor',
            'auth_form': auth_form,
            'is_captcha': is_captcha
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
