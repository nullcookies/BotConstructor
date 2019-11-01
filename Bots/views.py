from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Bot
from .forms import CreateBotForm, GetAccessToken


data = {}


class ShowBots(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'show_bots_url'

    def get(self, request):
        context = {
            'title': 'Your Bots - BotConstructor',
        }

        try:
            current_user_profile = Profile.objects.get(user=request.user)
            all_bots = Bot.objects.filter(owner=current_user_profile)
            if not all_bots:
                messages.error(request, 'No bots here')

            context.update({'all_bots': all_bots})
        except ObjectDoesNotExist:
            messages.error(request, 'Such object does not exist')

        return render(request, 'AllBots.html', context)


class CreateFileBot(View):
    def post(self, request):
        file_name = open('test_bot.py', 'w')
        file_name.close()
        return redirect('show_bots_url')


class CreateBot(View):
    def get(self, request):
        create_bot_form = CreateBotForm()

        context = {
            'title': 'Create Bot - BotConstructor',
            'create_bot_form': create_bot_form
        }
        return render(request, 'CreateBot.html', context)

    def post(self, request):
        create_bot_form = CreateBotForm(request.POST, request.FILES)
        current_user = Profile.objects.get(user=request.user)

        if create_bot_form.is_valid():
            access_token = create_bot_form.cleaned_data['access_token']
            file = create_bot_form.cleaned_data['file_script']

            current_bot = Bot.objects.create(
                access_token=access_token, file_script=file, owner=current_user)
            current_bot.save()

            return redirect('show_bots_url')

        context = {
            'title': 'Create Bot - BotConstructor',
            'create_bot_form': create_bot_form
        }
        return render(request, 'CreateBot.html', context)


class UpdateBot(View):
    def get(self, request, bot_id):
        current_bot = Bot.objects.get(id=bot_id)
        update_bot_form = CreateBotForm(instance=current_bot)

        context = {
            'title': 'Update Bot - BotConstructor',
            'update_bot_form': update_bot_form
        }
        return render(request, 'UpdateBot.html', context)

    def post(self, request, bot_id):
        current_bot = Bot.objects.get(id=bot_id)
        update_bot_form = CreateBotForm(
            request.POST, request.FILES, instance=current_bot)
        current_user = Profile.objects.get(user=request.user)

        if update_bot_form.is_valid():
            access_token = update_bot_form.cleaned_data['access_token']
            file = update_bot_form.cleaned_data['file_script']

            current_bot.access_token = access_token
            current_bot.file_script = file
            current_bot.owner = current_user
            current_bot.save()

            return redirect('show_bots_url')

        context = {
            'title': 'Update Bot - BotConstructor',
            'update_bot_form': update_bot_form
        }
        return render(request, 'UpdateBot.html', context)


class DeleteBot(View):
    def get(self, request, bot_id):
        context = {
            'title': 'Delete Bot - BotConstructor'
        }
        return render(request, 'DeleteBot.html', context)

    def post(self, request, bot_id):
        current_bot = Bot.objects.get(id=bot_id)
        current_bot.delete()
        return redirect('show_bots_url')


class CreateBotStepOne(View):
    def get(self, request):
        first_form = GetAccessToken()

        context = {
            'title': 'First Step - BotConstructor',
            'first_form': first_form
        }
        return render(request, 'FirstStep.html', context)

    def post(self, request):
        first_form = GetAccessToken(request.POST)

        if first_form.is_valid():
            access_token = first_form.cleaned_data['access_token']
            data['access_token'] = access_token
            print(access_token)

        context = {
            'title': 'First Step - BotConstructor',
            'first_form': first_form
        }
        return render(request, 'FirstStep.html', context)
