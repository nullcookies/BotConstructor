from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
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
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail.message import EmailMultiAlternatives
from sys import platform

import os
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

        self.context.update({
            'title': 'Profile - BotCostructor',
            'current_user': current_user
        })
        return render(request, 'Users/Profile.html', self.context)


class UserRegistration(View):
    context = {}

    def get(self, request):
        register_form = UserRegistrationForm()
        profile_form = ProfileForm()

        self.context.update({
            'title': 'Registration - BotConstructor',
            'register_form': register_form,
            'profile_form': profile_form
        })
        return render(request, 'Users/SignUp.html', self.context)

    def post(self, request):
        register_form = UserRegistrationForm(request.POST, request.FILES)
        profile_form = ProfileForm(request.POST)

        if 'count_registration' in request.session.keys():
            if request.session['count_registration'] < 2:
                if register_form.is_valid() and profile_form.is_valid():
                    recaptcha_response = request.POST.get(
                        'g-recaptcha-response')
                    validate_url = ('https://www.google.com/'
                                    'recaptcha/api/siteverify')
                    properties = {
                        'secret': settings.GOOGLE_SECRET_KEY,
                        'response': recaptcha_response
                    }
                    response = requests.get(validate_url, params=properties)
                    print(response)

                    if response.json()['success']:
                        username = register_form.cleaned_data['username']
                        first_name = register_form.cleaned_data['first_name']
                        last_name = register_form.cleaned_data['last_name']
                        email = register_form.cleaned_data['email']
                        password = register_form.cleaned_data['password_some']
                        password_confirm = register_form.cleaned_data[
                            'password_confirm'
                        ]
                        about = profile_form.cleaned_data['about']

                        some_user = User.objects.create_user(
                            username=username, email=email, password=password,
                            first_name=first_name, last_name=last_name)
                        some_user.is_active = False
                        some_user.save()

                        some_user_profile = Profile(
                            user=some_user, about=about)
                        some_user_profile.save()

                        current_site = get_current_site(request)
                        mail_subject = 'Activate your account'
                        message_content = render_to_string(
                            'ActiveEmail.html', {
                                'user': some_user,
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(
                                    force_bytes(some_user.pk)
                                ),
                                'token': account_activation_token.make_token(
                                    some_user),
                                'request': request
                            })
                        to_email = register_form.cleaned_data.get('email')

                        message = Mail(
                            from_email='noreply@bot-constructor.northeurope.'
                            'cloudapp.azure.com',
                            to_emails=to_email,
                            subject=mail_subject,
                            html_content=message_content)
                        print(message)
                        try:
                            sg = SendGridAPIClient(
                                'SG.48GCbtEqQtuRsR-25DMAZw.'
                                'FsF0nzFOdIno4UNc_JQZLqstiaONAIn3eTOv22cJGJg'
                            )
                            response = sg.send(message)
                            print(response.status_code)
                        except Exception as e:
                            print(e.message)

                        request.session['count_registration'] += 1

                        messages.error(
                            request,
                            'Now, a message will come to your mail'
                        )
                        return redirect('user_authentication_url')
                    else:
                        messages.error(request, 'Sorry, you are the robot')
            else:
                messages.error(
                    request,
                    'You have registered too many times...'
                )
                return redirect('user_authentication_url')
        else:
            if register_form.is_valid() and profile_form.is_valid():
                recaptcha_response = request.POST.get('g-recaptcha-response')
                validate_url = ('https://www.google.com/'
                                'recaptcha/api/siteverify')
                properties = {
                    'secret': settings.GOOGLE_SECRET_KEY,
                    'response': recaptcha_response
                }
                response = requests.get(validate_url, params=properties)
                print(response)

                if response.json()['success']:
                    username = register_form.cleaned_data['username']
                    first_name = register_form.cleaned_data['first_name']
                    last_name = register_form.cleaned_data['last_name']
                    email = register_form.cleaned_data['email']
                    password = register_form.cleaned_data['password_some']
                    password_confirm = register_form.cleaned_data[
                        'password_confirm'
                    ]
                    about = profile_form.cleaned_data['about']

                    some_user = User.objects.create_user(
                        username=username, email=email, password=password,
                        first_name=first_name, last_name=last_name)
                    some_user.is_active = False
                    some_user.save()

                    some_user_profile = Profile(
                        user=some_user, about=about)
                    some_user_profile.save()

                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account'
                    message_content = render_to_string('ActiveEmail.html', {
                        'user': some_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(
                            force_bytes(some_user.pk)
                        ),
                        'token': account_activation_token.make_token(
                            some_user),
                        'request': request
                    })
                    to_email = register_form.cleaned_data.get('email')

                    message = Mail(
                        from_email='noreply@bot-constructor.northeurope.'
                        'cloudapp.azure.com',
                        to_emails=to_email,
                        subject=mail_subject,
                        html_content=message_content)
                    print(message)
                    try:
                        sg = SendGridAPIClient(
                            'SG.48GCbtEqQtuRsR-25DMAZw.'
                            'FsF0nzFOdIno4UNc_JQZLqstiaONAIn3eTOv22cJGJg'
                        )
                        response = sg.send(message)
                        print(response.status_code)
                    except Exception as e:
                        print(e.message)

                    request.session['count_registration'] = 1

                    messages.error(
                        request,
                        'Now, a message will come to your mail'
                    )
                    return redirect('user_authentication_url')
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
        update_form = UpdatingForm(instance=request.user)
        getted_current_user = Profile.objects.get(user=request.user)
        update_profile_form = ProfileForm(instance=getted_current_user)
        update_image_form = UpdateImageForm(instance=getted_current_user)

        self.context.update({
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form,
            'update_profile_form': update_profile_form,
            'update_image_form': update_image_form,
            'getted_current_user': getted_current_user
        })
        return render(request, 'Users/UpdateProfile.html', self.context)

    def post(self, request):
        update_form = UpdatingForm(request.POST, instance=request.user)
        current_user = User.objects.get(id=int(request.user.id))
        getted_current_user = Profile.objects.get(user=request.user)
        update_profile_form = ProfileForm(
            request.POST, instance=getted_current_user)
        update_image_form = UpdateImageForm(
            request.POST, request.FILES, instance=getted_current_user)

        if update_form.is_valid() and update_profile_form.is_valid() and \
                update_image_form.is_valid():
            username = update_form.cleaned_data['username']
            first_name = update_form.cleaned_data['first_name']
            last_name = update_form.cleaned_data['last_name']
            email = update_form.cleaned_data['email']
            about = update_profile_form.cleaned_data['about']

            current_user.username = username
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            current_user.save()

            getted_current_user.about = about
            getted_current_user.save()

            update_image_form.save()

            new_user = authenticate(
                username=username, password=current_user.password)
            login(request, new_user)
            return redirect('profile_url')

        self.context.update({
            'title': 'Update Profile - BotConstructor',
            'update_form': update_form,
            'update_profile_form': update_profile_form,
            'update_image_form': update_image_form,
            'getted_current_user': getted_current_user
        })
        return render(request, 'Users/UpdateProfile.html', self.context)


# class UserDelete(View):
#     def get(self, request):
#         context = {
#             'title': 'Delete User - BotConstructor',
#         }
#         return render(request, 'Users/DeleteUser.html', context)

#     def post(self, request):
#         user = User.objects.get(id=int(request.user.id))
#         user.delete()
#         return redirect('base_view_url')
