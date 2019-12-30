from django.urls import path

from .views import *

urlpatterns = [
    path('yourBots/', ShowBots.as_view(), name='show_bots_url'),
    path('createBot/firstStep/',
         CreateBotStepOne.as_view(), name='create_bot_first_step_url'),
    path('createBot/thirdStep/',
         CreateBotStepThree.as_view(), name='create_bot_third_step_url'),
    path('createBot/secondStep/text/',
         CreateTextField.as_view(), name='create_bot_second_step_text_url'),
    path('createBot/secondStep/text/delete/<int:button_id>/',
         DeleteTextField.as_view(),
         name='create_bot_second_step_text_delete_url'),
    path('createBot/secondStep/text/update/', UpdateTextField.as_view(),
         name='create_bot_second_step_text_update_url'),
    path('createBot/secondStep/replyMarkup/', CreateReplyMarkupField.as_view(),
         name='create_bot_second_step_reply_markup_url'),
    path('createBot/secondStep/replyMarkup/replyButtons/',
         CreateReplyButtonsField.as_view(),
         name='create_bot_second_step_reply_buttons_url'),
    path(
        'createBot/secondStep/replyMarkup/deleteReplyButton/<int:markup_id>/\
<int:button_id>/',
        DeleteReplyButtonField.as_view(),
        name='create_bot_second_step_reply_button_delete_url'),
    path('createBot/secondStep/replyMarkup/deleteReplyMarkup/<int:markup_id>/',
         DeleteReplyMarkupField.as_view(),
         name='create_bot_second_step_reply_markup_delete_url'),
    path('createBot/secondStep/replyMarkup/updateReplyMarkup/',
         UpdateReplyMarkupField.as_view(),
         name='create_bot_second_step_reply_markup_update_url'),
    path('createBot/secondStep/replyMarkup/updateReplyButtons/',
         UpdateReplyButtonsField.as_view(),
         name='create_bot_second_step_reply_buttons_update_url'),
    path('createBot/secondStep/inlineMarkup/',
         CreateInlineMarkupField.as_view(),
         name='create_bot_second_step_inline_markup_url'),
    path('createBot/secondStep/nextStep/', GenerateFile.as_view(),
         name='create_bot_second_step_next_step_url'),
    path('createBot/thirdStep/downloadConfig/',
         Download.config, name='download_config_url'),
    path('createBot/thirdStep/downloadScript/',
         Download.script, name='download_script_url'),
    path('updateBot/<int:bot_id>/',
         UpdateBot.as_view(), name='update_bot_url'),
    path('deleteBot/<int:bot_id>/', DeleteBot.as_view(), name='delete_bot_url')
]
