from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import resolve

from ..functions import *
from ..forms import InlineButton


class CreateInlineButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, token: str):
        inline_markup_elements = enumerate_elements(request,
                                                    token=token,
                                                    get_object='inline_markup')
        inline_button_form = InlineButton()

        current_url = resolve(request.path_info).url_name
        if inline_markup_elements == [] \
                and current_url != 'create_bot_second_step_inline_markup_url':
            return redirect(
                'create_bot_second_step_inline_markup_url',
                token=token
            )

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        inline_markup_elements = enumerate_elements(request,
                                                    token=token,
                                                    get_object='inline_markup')
        inline_button_form = InlineButton(request.POST)

        if inline_button_form.is_valid():
            text = inline_button_form.cleaned_data['text']
            url = inline_button_form.cleaned_data['url']
            callback = inline_button_form.cleaned_data['callback']
            switch_inline = inline_button_form.cleaned_data['switch_inline']
            switch_inline_current = inline_button_form.cleaned_data[
                'switch_inline_current'
            ]
            print(text, url, callback, switch_inline, switch_inline_current)

            if callback == '':
                callback = False

            if url == '':
                url = False

            if switch_inline == '':
                switch_inline = False

            if switch_inline_current == '':
                switch_inline_current = False

            path = open_configuration(request, token)
            with open(path, 'r+', encoding='utf-8') as file:
                object_config = json.load(file)

                try:
                    object_config['inline_markup'][-1][
                        'buttons'
                    ].append({
                        'text': text,
                        'url': url,
                        'callback': callback,
                        'switch_inline': switch_inline,
                        'switch_inline_current': switch_inline_current
                    })
                except KeyError:
                    object_config['inline_markup'][-1]['buttons'] = [{
                        'text': text,
                        'url': url,
                        'callback': callback,
                        'switch_inline': switch_inline,
                        'switch_inline_current': switch_inline_current
                    }]
                file.seek(0)
                json.dump(object_config, file, indent=4, ensure_ascii=False)
                len_text = len(object_config['inline_markup']) - 1
                len_button = len(
                    object_config['inline_markup'][-1]['buttons']) - 1

                return JsonResponse({
                    'token': token,
                    'csrf': request.POST.get('csrfmiddlewaretoken'),
                    'text': text,
                    'url': url,
                    'callback': callback,
                    'switch_inline': switch_inline,
                    'switch_inline_current': switch_inline_current,
                    'len_text': len_text,
                    'len_button': len_button
                })
        else:
            print(inline_button_form.errors)
            return JsonResponse({
                'inline_button_error': inline_button_form.errors
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateInlineButtonsField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_buttons_url'
    context = {}

    def post(self, request, token: str):
        if request.POST.get('action') == 'update_inline_button':
            text = request.POST.get('text')
            callback = request.POST.get('callback')
            url = request.POST.get('url')
            switch_inline = request.POST.get('switch_inline')
            switch_inline_current = request.POST.get('switch_inline_current')
            markup_id = int(request.POST.get('markup_id'))
            button_id = int(request.POST.get('button_id'))

            if callback == '':
                callback = False

            if url == '':
                url = False

            if switch_inline == '':
                switch_inline = False

            if switch_inline_current == '':
                switch_inline_current = False

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            inline_markup_object = object_config['inline_markup']
            inline_markup_object[markup_id]['buttons'][button_id][
                'text'
            ] = text
            inline_markup_object[markup_id]['buttons'][button_id]['url'] = url
            inline_markup_object[markup_id]['buttons'][button_id][
                'callback'
            ] = callback
            inline_markup_object[markup_id]['buttons'][button_id][
                'switch_inline'
            ] = switch_inline
            inline_markup_object[markup_id]['buttons'][button_id][
                'switch_inline_current'
            ] = switch_inline_current

            object_config['inline_markup'] = inline_markup_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return redirect(
                'create_bot_second_step_inline_buttons_url',
                token=token
            )

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class DeleteInlineButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'
    context = {}

    def get(self, request, token: str):
        if request.GET.get('action') == 'delete_inline_button':
            markup_id = int(request.GET.get('markup_id'))
            button_id = int(request.GET.get('button_id'))

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            inline_button_object = object_config[
                'inline_markup'
            ][markup_id]['buttons']
            inline_button_object.remove(inline_button_object[button_id])

            object_config[
                'inline_markup'
            ][markup_id]['buttons'] = inline_button_object
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
