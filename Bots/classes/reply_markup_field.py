from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

from ..functions import *
from ..forms import ReplyMarkup


class CreateReplyMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request, token: str):
        reply_markup_elements = enumerate_elements(request,
                                                   token=token,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(request=request, token=token)

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        reply_markup_elements = enumerate_elements(request,
                                                   token=token,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(
            request.POST, request=request, token=token
        )
        resize_keyboard = request.POST.get('resize_keyboard')
        one_time_keyboard = request.POST.get('one_time_keyboard')
        selective_keyboard = request.POST.get('selective_keyboard')
        csrf = request.POST.get('csrfmiddlewaretoken')

        if resize_keyboard == 'true':
            resize_keyboard = True
        else:
            resize_keyboard = False

        if one_time_keyboard == 'true':
            one_time_keyboard = True
        else:
            one_time_keyboard = False

        if selective_keyboard == 'true':
            selective_keyboard = True
        else:
            selective_keyboard = False

        print(request.POST)
        if reply_markup_form.is_valid():
            react_text = reply_markup_form.cleaned_data['react_text']
            row_width = reply_markup_form.cleaned_data['row_width']
            response_text = reply_markup_form.cleaned_data[
                'response_text_markup'
            ]

            path = open_configuration(request, token)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['reply_markup'].append({
                        'resize_keyboard': resize_keyboard,
                        'one_time_keyboard': one_time_keyboard,
                        'selective': selective_keyboard,
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    })
                except KeyError:
                    object_config['reply_markup'] = [{
                        'resize_keyboard': resize_keyboard,
                        'one_time_keyboard': one_time_keyboard,
                        'selective': selective_keyboard,
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)
                len_text = len(object_config['reply_markup']) - 1

            return JsonResponse({
                'resize_keyboard': resize_keyboard,
                'one_time_keyboard': one_time_keyboard,
                'selective': selective_keyboard,
                'react_text': react_text,
                'row_width': row_width,
                'response_text': response_text,
                'csrf': csrf,
                'token': token,
                'len_text': len_text
            })
        else:
            return JsonResponse({
                'reply_markup_error': reply_markup_form.errors
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'
    context = {}

    def post(self, request, token: str):
        if request.POST.get('action') == 'update_reply_markup':
            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            react_text = request.POST.get('react_text')
            row_width = int(request.POST.get('row_width'))
            response_text = request.POST.get('response_text')
            resize_keyboard = request.POST.get('resize_keyboard')
            one_time_keyboard = request.POST.get('one_time_keyboard')
            selective = request.POST.get('selective')

            index = int(request.POST.get('index'))

            if resize_keyboard == 'true':
                resize_keyboard = True
            else:
                resize_keyboard = False

            if one_time_keyboard == 'true':
                one_time_keyboard = True
            else:
                one_time_keyboard = False

            if selective == 'true':
                selective = True
            else:
                selective = False

            reply_markup_object = object_config['reply_markup']

            reply_markup_object[index]['react_text'] = react_text
            reply_markup_object[index]['row_width'] = row_width
            reply_markup_object[index]['response_text'] = response_text
            reply_markup_object[index]['resize_keyboard'] = resize_keyboard
            reply_markup_object[index]['one_time_keyboard'] = one_time_keyboard
            reply_markup_object[index]['selective'] = selective

            object_config['reply_markup'] = reply_markup_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4, ensure_ascii=False)
            return JsonResponse({})

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class DeleteReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'
    context = {}

    def get(self, request, token: str):
        if request.GET.get('action') == 'delete_reply_markup':
            markup_id = int(request.GET.get('button_id'))
            print(markup_id)

            path = open_configuration(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                object_config = json.load(file)

            reply_markup_object = object_config['reply_markup']
            reply_markup_object.remove(reply_markup_object[markup_id])

            object_config['reply_markup'] = reply_markup_object
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(object_config, file, indent=4,
                          ensure_ascii=False)

            return JsonResponse({
                'markup_id': markup_id
            })

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)
