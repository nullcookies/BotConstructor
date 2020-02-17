from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..functions import *
from ..forms import InlineMarkup


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

        if inline_markup_form.is_valid():
            row_width = inline_markup_form.cleaned_data['row_width']
            response_text = inline_markup_form.cleaned_data['response_text']
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
                return redirect(
                    'create_bot_second_step_inline_buttons_url',
                    token=token
                )

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

    def post(self, request, token: str):
        data = dict(request.POST)
        print(data)

        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        inline_markup_object = object_config['inline_markup']
        final_data = []
        index = int(list(data.items())[1][0].split('_')[-1])

        for inline_markup in data.items():
            if inline_markup[0] != 'csrfmiddlewaretoken':
                text = inline_markup[1][0]
                final_data.append([index, text])

        for item in range(len(inline_markup_object)):
            if item == index:
                inline_markup_object[item][
                    'react_text'
                ] = final_data[1][1].strip()
                inline_markup_object[item][
                    'response_text'
                ] = final_data[0][1].strip()
                inline_markup_object[item]['row_width'] = final_data[2][1]

        object_config['inline_markup'] = inline_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect(
            'create_bot_second_step_inline_markup_url',
            token=token
        )


class DeleteInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, token: str, markup_id: int):
        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_markup_object = object_config['inline_markup']
        reply_markup_object.remove(reply_markup_object[markup_id])

        object_config['inline_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect(
            'create_bot_second_step_inline_markup_url',
            token=token
        )
