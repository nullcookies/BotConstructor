from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve
from django.http import JsonResponse

from ..functions import *
from ..forms import ReplyButton


class CreateReplyButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'
    required_fields = [
        'request_contact',
        'request_location'
    ]

    def get(self, request, token: str):
        reply_markup_elements = enumerate_elements(request,
                                                   token=token,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton()
        current_url = resolve(request.path_info).url_name
        print(current_url)
        if reply_markup_elements == [] \
                and current_url != 'create_bot_second_step_reply_markup_url':
            return redirect(
                'create_bot_second_step_reply_markup_url',
                token=token
            )

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        reply_markup_elements = enumerate_elements(request,
                                                   token=token,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton(request.POST)

        if request.POST.get('action') == 'create_reply_button':
            if reply_button_form.is_valid():
                response_text = reply_button_form.cleaned_data[
                    'response_text'
                ]
                request_contact = request.POST.get('request_contact')
                request_location = request.POST.get('request_location')

                if request_contact == 'true':
                    request_contact = True
                else:
                    request_contact = False

                if request_location == 'true':
                    request_location = True
                else:
                    request_location = False

                path = open_configuration(request, token)
                with open(path, 'r+', encoding='utf-8') as file_name:
                    object_config = json.load(file_name)

                    try:
                        object_config['reply_markup'][-1]['buttons'].append({
                            'response_text': response_text,
                            'request_contact': request_contact,
                            'request_location': request_location
                        })
                    except KeyError:
                        object_config['reply_markup'][-1]['buttons'] = [{
                            'response_text': response_text,
                            'request_contact': request_contact,
                            'request_location': request_location
                        }]
                    file_name.seek(0)
                    json.dump(object_config, file_name,
                              indent=4, ensure_ascii=False)
                    len_text = len(object_config['reply_markup']) - 1
                    len_button = len(
                        object_config['reply_markup'][-1]['buttons']) - 1

                return JsonResponse({
                    'response_text': response_text,
                    'request_contact': request_contact,
                    'request_location': request_location,
                    'token': token,
                    'csrf': request.POST.get('csrfmiddlewaretoken'),
                    'len_text': len_text,
                    'len_button': len_button
                })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyButtonsField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'
    context = {}

    def post(self, request, token: str):
        if request.POST.get('action') == 'delete_reply_button':
            response_text = request.POST.get('response_text')
            req_con = request.POST.get('req_con')
            req_loc = request.POST.get('req_loc')
            markup_id = int(request.POST.get('markup_id'))
            button_id = int(request.POST.get('button_id'))

            if req_con == 'true':
                req_con = True
            else:
                req_con = False

            if req_loc == 'true':
                req_loc = True
            else:
                req_loc = False

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            reply_markup_object = object_config['reply_markup']
            reply_markup_object[markup_id]['buttons'][button_id][
                'response_text'
            ] = response_text
            reply_markup_object[markup_id]['buttons'][button_id][
                'request_contact'
            ] = req_con
            reply_markup_object[markup_id]['buttons'][button_id][
                'request_location'
            ] = req_loc

            object_config['reply_markup'] = reply_markup_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({})

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class DeleteReplyButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'
    context = {}

    def get(self, request, token: str):
        if request.GET.get('action') == 'delete_reply_button':
            markup_id = int(request.GET.get('markup_id'))
            button_id = int(request.GET.get('button_id'))

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            reply_button_object = object_config[
                'reply_markup'
            ][markup_id]['buttons']
            reply_button_object.remove(reply_button_object[button_id])

            object_config[
                'reply_markup'
            ][markup_id]['buttons'] = reply_button_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({
                'markup_id': markup_id,
                'button_id': button_id
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)
