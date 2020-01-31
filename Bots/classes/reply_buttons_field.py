from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def get(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton(request.POST)

        if reply_button_form.is_valid():
            response_text = reply_button_form.cleaned_data[
                'response_text'
            ]
            radio_buttons = reply_button_form.cleaned_data[
                'radio_buttons'
            ]

            check_radio = {}
            for item in self.required_fields:
                if item in radio_buttons:
                    check_radio[item] = True
                else:
                    check_radio[item] = False

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['reply_markup'][-1]['buttons'].append({
                        'response_text': response_text,
                        'request_contact': check_radio['request_contact'],
                        'request_location': check_radio['request_location']
                    })
                except KeyError:
                    object_config['reply_markup'][-1]['buttons'] = [{
                        'response_text': response_text,
                        'request_contact': check_radio['request_contact'],
                        'request_location': check_radio['request_location']
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)
            return redirect('create_bot_second_step_reply_buttons_url')

        reply_markup_elements = enumerate_elements(request, 'reply_markup')
        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyButtonsField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'

    required_radios = [
        'request_contact',
        'request_location'
    ]

    def post(self, request):
        data = dict(request.POST)
        print(data)
        obligatory_fields = [
            'response_text'
        ]

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = (int(list(data.items())[1][0].split('_')[-2]),
                 int(list(data.items())[1][0].split('_')[-1]))
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=False, index=index,
                                     checkboxes=self.required_radios,
                                     data=data)

        for item in self.required_radios:
            if item in list(data.values())[-1]:
                final_data[item] = [index, True]
            else:
                final_data[item] = [index, False]

        print(final_data)

        reply_markup_object = object_config['reply_markup']
        reply_markup_object[index[0]]['buttons'][index[1]][
            'response_text'
        ] = final_data['response_text'][1].strip()
        reply_markup_object[index[0]]['buttons'][index[1]][
            'request_contact'
        ] = final_data['request_contact'][1]
        reply_markup_object[index[0]]['buttons'][index[1]][
            'request_location'
        ] = final_data['request_location'][1]

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_buttons_url')


class DeleteReplyButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request, markup_id: int, button_id: int):
        path = open_configuration(request)
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
        return redirect('create_bot_second_step_reply_markup_url')
