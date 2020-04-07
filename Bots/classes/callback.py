from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import CallbackForm
from ..functions import *
from django.http import JsonResponse


class CreateCallbackField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_callback_url'
    context = {}

    def get(self, request, token: str):
        callback_form = CallbackForm(
            request=request,
            token=token
        )
        callback_elements = enumerate_elements(
            request, token=token, get_object='callbacks'
        )

        FIELDS_REACT = []
        FIELDS_CALLBACK = []

        path = open_configuration(request=request, token=token)
        with open(path, 'r', encoding='utf-8') as file:
            some = json.load(file)

        # ! Get react text into a list
        # if 'reply_markup' in some:
        #     for item in some['reply_markup']:
        #         FIELDS_REACT.append(
        #             (f'{item["react_text"]}_key', item['react_text'])
        #         )

        if 'text' in some:
            for item in some['text']:
                FIELDS_REACT.append(
                    (f'{item["react_text"]}_key', item['react_text'])
                )

        # if 'inline_markup' in some:
        #     for item in some['inline_markup']:
        #         FIELDS_REACT.append(
        #             (f'{item["react_text"]}_key', item['react_text'])
        #         )

        # ! Get callbacks into a list
        if 'inline_markup' in some:
            for item in some['inline_markup']:
                for button in item['buttons']:
                    print(button['callback'])
                    if button['callback'] is not False:
                        FIELDS_CALLBACK.append(
                            (f'{button["callback"]}_key', button['callback'])
                        )

        self.context.update({
            'title': 'CallBack - BotConstructor',
            'callback_form': callback_form,
            'token': token,
            'fields_callback': FIELDS_CALLBACK,
            'fields_react': FIELDS_REACT,
            'callback_elements': callback_elements
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token):
        callback_form = CallbackForm(
            request.POST,
            request=request,
            token=token
        )
        callback_elements = enumerate_elements(
            request, token=token, get_object='callbacks'
        )

        if request.POST.get('action') == 'create_callback':
            if callback_form.is_valid():
                callback = callback_form.cleaned_data['callback_text']
                react_text = callback_form.cleaned_data['react_text']
                csrf = request.POST.get('csrfmiddlewaretoken')

                path = open_configuration(request, token)
                with open(path, 'r+', encoding='utf-8') as file:
                    object_config = json.load(file)
                    try:
                        object_config['callbacks'].append({
                            'callback': callback,
                            'react_text': react_text
                        })
                    except KeyError:
                        object_config['callbacks'] = [{
                            'callback': callback,
                            'react_text': react_text,
                        }]
                    file.seek(0)
                    json.dump(object_config, file,
                              indent=4, ensure_ascii=False)
                    len_text = len(object_config['text']) - 1

                    return JsonResponse({
                        'callback': callback,
                        'react_text': react_text,
                        'len_text': len_text,
                        'csrf': csrf,
                        'token': token
                    })
            else:
                return JsonResponse({
                    'callback_error': callback_form.errors
                })

        self.context.update({
            'title': 'CallBack - BotConstructor',
            'callback_form': callback_form,
            'token': token,
            'callback_elements': callback_elements
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateCallbackField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_callback_url'
    context = {}

    def post(self, request, token):
        if request.POST.get('action') == 'update_callback':
            react_text = request.POST.get('react_text')
            callback_text = request.POST.get('callback_text')
            print(react_text, callback_text)

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            index = int(request.POST.get('index'))
            callback_object = object_config['callbacks']

            callback_object[index]['callback'] = callback_text
            callback_object[index]['react_text'] = react_text

            object_config['callbacks'] = callback_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({})

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class DeleteCallbackField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_callback_url'
    context = {}

    def get(self, request, token):
        if request.GET.get('action') == 'delete_callback':
            button_id = int(request.GET.get('button_id'))
            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            callback_object = object_config['callbacks']
            callback_object.remove(callback_object[button_id])

            object_config['callbacks'] = callback_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({
                'button_id': button_id
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)
