from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..functions import *
from ..forms import ReplyMarkup


class CreateReplyMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    required_fields = [
        'resize_keyboard',
        'one_time_keyboard',
        'selective'
    ]

    def get(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(request=request)

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(request.POST, request=request)

        if reply_markup_form.is_valid():
            react_text = reply_markup_form.cleaned_data['react_text']
            row_width = reply_markup_form.cleaned_data['row_width']
            response_text = reply_markup_form.cleaned_data[
                'response_text_markup'
            ]
            keyboard_settings = reply_markup_form.cleaned_data['checkboxes']

            check_checkboxes = {}
            for item in self.required_fields:
                if item in keyboard_settings:
                    check_checkboxes[item] = True
                else:
                    check_checkboxes[item] = False

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['reply_markup'].append({
                        'resize_keyboard': check_checkboxes['resize_keyboard'],
                        'one_time_keyboard': check_checkboxes[
                            'one_time_keyboard'
                        ],
                        'selective': check_checkboxes['selective'],
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    })
                except KeyError:
                    object_config['reply_markup'] = [{
                        'resize_keyboard': check_checkboxes['resize_keyboard'],
                        'one_time_keyboard': check_checkboxes[
                            'one_time_keyboard'
                        ],
                        'selective': check_checkboxes['selective'],
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)

            reply_markup_elements = enumerate_elements(request,
                                                       'reply_markup')
            return redirect('create_bot_second_step_reply_buttons_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    checkboxes = [
        'resize_keyboard',
        'one_time_keyboard',
        'selective'
    ]

    def post(self, request):
        obligatory_fields = [
            'resize_keyboard',
            'one_time_keyboard',
            'selective',
            'react_text',
            'row_width',
            'response_text_markup'
        ]
        data = dict(request.POST)

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = int(list(data.items())[1][0].split('_')[-1])
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=True, checkboxes=self.checkboxes,
                                     index=index, data=data)

        reply_markup_object = object_config['reply_markup']

        reply_markup_object[index]['react_text'] = final_data[
            'react_text'
        ][1].strip()
        reply_markup_object[index]['row_width'] = int(
            final_data['row_width'][1].strip())
        reply_markup_object[index]['response_text'] = final_data[
            'response_text_markup'
        ][1].strip()
        reply_markup_object[index]['resize_keyboard'] = final_data[
            'resize_keyboard'
        ][1]
        reply_markup_object[index]['one_time_keyboard'] = final_data[
            'one_time_keyboard'
        ][1]
        reply_markup_object[index]['selective'] = final_data['selective'][1]

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class DeleteReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request, markup_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_markup_object = object_config['reply_markup']
        reply_markup_object.remove(reply_markup_object[markup_id])

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')
