from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..functions import *
from ..forms import InlineMarkup
from django.http import JsonResponse


class CreateInlineMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, token: str):
        inline_markup_elements = enumerate_elements(request,
                                                    token=token,
                                                    get_object='inline_markup')
        inline_markup_form = InlineMarkup()
        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_markup_form': inline_markup_form,
            'inline_markup_elements': inline_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        inline_markup_elements = enumerate_elements(request,
                                                    token=token,
                                                    get_object='inline_markup')
        inline_markup_form = InlineMarkup(request.POST)

        print(request.POST)
        if request.POST.get('action') == 'create_inline_markup':
            if inline_markup_form.is_valid():
                print(inline_markup_form.cleaned_data)
                row_width = int(inline_markup_form.cleaned_data['row_width'])
                response_text = inline_markup_form.cleaned_data[
                    'response_text'
                ]
                react_text = inline_markup_form.cleaned_data['react_text']

                path = open_configuration(request, token)
                with open(path, 'r+', encoding='utf-8') as file:
                    object_config = json.load(file)

                    try:
                        object_config['inline_markup'].append({
                            'row_width': row_width,
                            'response_text': response_text,
                            'react_text': react_text
                        })
                    except KeyError:
                        object_config['inline_markup'] = [{
                            'row_width': row_width,
                            'react_text': react_text,
                            'response_text': response_text
                        }]
                    file.seek(0)
                    json.dump(object_config, file,
                              indent=4, ensure_ascii=False)
                    len_text = len(object_config['inline_markup']) - 1

                    return JsonResponse({
                        'react_text': react_text,
                        'response_text': response_text,
                        'row_width': row_width,
                        'token': token,
                        'csrf': request.POST.get('csrfmiddlewaretoken'),
                        'len_text': len_text
                    })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_markup_form': inline_markup_form,
            'inline_markup_elements': inline_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'
    context = {}

    def post(self, request, token: str):
        data = dict(request.POST)
        print(data)

        if request.POST.get('action') == 'update_inline_markup':
            response_text = request.POST.get('response_text')
            react_text = request.POST.get('react_text')
            row_width = int(request.POST.get('row_width'))
            index = int(request.POST.get('markup_id'))

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            inline_markup_object = object_config['inline_markup']
            inline_markup_object[index]['react_text'] = react_text
            inline_markup_object[index]['response_text'] = response_text
            inline_markup_object[index]['row_width'] = row_width
            object_config['inline_markup'] = inline_markup_object

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({})

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class DeleteInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'
    context = {}

    def get(self, request, token: str):
        if request.GET.get('action') == 'delete_inline_markup':
            markup_id = int(request.GET.get('button_id'))

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            reply_markup_object = object_config['inline_markup']
            reply_markup_object.remove(reply_markup_object[markup_id])

            object_config['inline_markup'] = reply_markup_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({
                'markup_id': markup_id
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)
