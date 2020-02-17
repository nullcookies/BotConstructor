from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..functions import *
from ..forms import TextForm


class CreateTextField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def get(self, request, token: str):
        text_elements = enumerate_elements(request,
                                           token=token, get_object='text')
        text_form = TextForm(request=request, token=token)

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'text_elements': text_elements,
            'text_form': text_form,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        text_elements = enumerate_elements(request,
                                           token=token, get_object='text')
        text_form = TextForm(request.POST, request=request, token=token)

        if text_form.is_valid():
            response_text = text_form.cleaned_data['response_text']
            react_text = text_form.cleaned_data['react_text'].strip()

            if 'remove_reply_markup' in text_form.cleaned_data.keys():
                if text_form.cleaned_data['remove_reply_markup'] == []:
                    remove_reply_markup = False
                else:
                    remove_reply_markup = True
            else:
                remove_reply_markup = False

            path = open_configuration(request, token)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['text'].append({
                        'response_text': response_text,
                        'react_text': react_text,
                        'remove_reply_markup': remove_reply_markup
                    })
                except KeyError:
                    object_config['text'] = [{
                        'response_text': response_text,
                        'react_text': react_text,
                        'remove_reply_markup': remove_reply_markup
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)
            return redirect(
                'create_bot_second_step_text_url',
                token=token
            )

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'text_elements': text_elements,
            'text_form': text_form,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateTextField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def post(self, request, token: str):
        data = dict(request.POST)

        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['text']
        final_data = []
        for button in data.items():
            try:
                index = int(button[0].split('_')[-1])
                text = button[1][0]
                final_data.append([index, text])
            except ValueError:
                pass

        for item in range(len(text_object)):
            if item == final_data[0][0]:
                text_object[item]['react_text'] = final_data[0][1].strip()
                text_object[item]['response_text'] = final_data[1][1]

                try:
                    if final_data[2][1] == 'on':
                        text_object[item][
                            'remove_reply_markup'
                        ] = True
                except IndexError:
                    text_object[item][
                        'remove_reply_markup'
                    ] = False

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect(
            'create_bot_second_step_text_url',
            token=token
        )


class DeleteTextField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def get(self, request, button_id: int, token: str):
        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['text']
        text_object.remove(text_object[button_id])

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect(
            'create_bot_second_step_text_url',
            token=token
        )
