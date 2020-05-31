from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse

from ..forms import TipsForm
from ..functions import open_configuration

import json


class Tips(LoginRequiredMixin, View):
    login_url = "/signIn/"
    redirect_field_name = "bot_tips"

    def get(self, request, token: str):
        tips_form = TipsForm()

        path: str = open_configuration(request, token)
        with open(path, 'r', encoding="utf8") as file:
            object_config = json.load(file)

        context = {
            'title': 'Tips - Bot Constrcutor',
            "tips_form": tips_form,
            "token": token,
            "object_config": object_config
        }
        return render(request, 'Tips.html', context)

    def post(self, request, token: str):
        tips_form = TipsForm(request.POST)

        if tips_form.is_valid():
            tips = tips_form.cleaned_data["tips"]
            m_exception = True if "message_exception" in tips else False

            path: str = open_configuration(request, token)
            with open(path, 'r+', encoding="utf8") as file:
                object_config = json.load(file)

                object_config["message_exception"] = m_exception

                file.seek(0)
                file.truncate()
                json.dump(
                    object_config, file,
                    indent=4, ensure_ascii=False
                )
            return JsonResponse({})

        context = {
            'title': 'Tips - Bot Constrcutor',
            "tips_form": tips_form,
            "token": token,
            "object_config": object_config
        }
        return render(request, 'Tips.html', context)
