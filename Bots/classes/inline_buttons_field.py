from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..functions import *
from ..forms import InlineButton


class CreateInlineButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request):
        inline_markup_elements = enumerate_elements(request,
                                                    get_object='inline_markup')
        inline_button_form = InlineButton()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        inline_markup_elements = enumerate_elements(request,
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

            path = open_configuration(request)
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
                return redirect('create_bot_second_step_inline_buttons_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_buttons_url'

    def post(self, request):
        data = dict(request.POST)
        print(data)

        obligatory_fields = [
            'text_inline',
            'url_inline',
            'callback',
            'switch_inline',
            'switch_inline_current'
        ]

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = (int(list(data.items())[1][0].split('_')[-2]),
                 int(list(data.items())[1][0].split('_')[-1]))
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=False, index=index, data=data)

        inline_markup_object = object_config['inline_markup']
        print(inline_markup_object)
        inline_markup_object[index[0]]['buttons'][index[1]][
            'text'
        ] = final_data['text_inline'][1].strip()
        inline_markup_object[index[0]]['buttons'][index[1]][
            'url'
        ] = final_data['url_inline'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'callback'
        ] = final_data['callback'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'switch_inline'
        ] = final_data['switch_inline'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'switch_inline_current'
        ] = final_data['switch_inline_current'][1]

        object_config['inline_markup'] = inline_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_inline_buttons_url')


class DeleteInlineButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, markup_id: int, button_id: int):
        path = open_configuration(request)
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
        return redirect('create_bot_second_step_inline_markup_url')
