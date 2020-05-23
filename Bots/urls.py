from django.urls import path

from .views import *

urlpatterns = [
    path(
        'yourBots/',
        ShowBots.as_view(),
        name='show_bots_url'
    ),
    path(
        'createBot/firstStep/',
        CreateBotStepOne.as_view(),
        name='create_bot_first_step_url'
    ),
    path(
        'createBot/thirdStep/<str:token>/',
        CreateBotStepThree.as_view(),
        name='create_bot_third_step_url'
    ),
    path(
        'createBot/secondStep/<str:token>/text/',
        CreateTextField.as_view(),
        name='create_bot_second_step_text_url'
    ),
    path(
        'createBot/secondStep/<str:token>/text/delete/',
        DeleteTextField.as_view(),
        name='create_bot_second_step_text_delete_url'
    ),
    path(
        'createBot/secondStep/<str:token>/text/update/',
        UpdateTextField.as_view(),
        name='create_bot_second_step_text_update_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/',
        CreateReplyMarkupField.as_view(),
        name='create_bot_second_step_reply_markup_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/replyButtons/',
        CreateReplyButtonsField.as_view(),
        name='create_bot_second_step_reply_buttons_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/deleteReplyButton/',
        DeleteReplyButtonField.as_view(),
        name='create_bot_second_step_reply_button_delete_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/deleteInlineButton/',
        DeleteInlineButtonField.as_view(),
        name='create_bot_second_step_inline_buttons_delete_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/deleteReplyMarkup/',
        DeleteReplyMarkupField.as_view(),
        name='create_bot_second_step_reply_markup_delete_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/updateReplyMarkup/',
        UpdateReplyMarkupField.as_view(),
        name='create_bot_second_step_reply_markup_update_url'
    ),
    path(
        'createBot/secondStep/<str:token>/replyMarkup/updateReplyButtons/',
        UpdateReplyButtonsField.as_view(),
        name='create_bot_second_step_reply_buttons_update_url'
    ),
    path(
        'createBot/secondStep/<str:token>/inlineMarkup/',
        CreateInlineMarkupField.as_view(),
        name='create_bot_second_step_inline_markup_url'
    ),
    path(
        'createBot/secondStep/<str:token>/inlineMarkup/inlineButtons/',
        CreateInlineButtonsField.as_view(),
        name='create_bot_second_step_inline_buttons_url'
    ),
    path(
        'createBot/secondStep/<str:token>/inlineMarkup/updateInlineButtons',
        UpdateInlineButtonsField.as_view(),
        name='create_bot_second_step_inline_buttons_update_url'
    ),
    path(
        'createBot/secondStep/<str:token>/inlineMarkup/updateInlineMarkup',
        UpdateInlineMarkupField.as_view(),
        name='create_bot_second_step_inline_markup_update_url'
    ),
    path(
        'createBot/secondStep/<str:token>/inlineMarkup/deleteInlineMarkup/',
        DeleteInlineMarkupField.as_view(),
        name='create_bot_second_step_inline_markup_delete_url'
    ),
    path(
        'createBot/secondStep/<str:token>/nextStep/',
        GenerateFile.as_view(),
        name='create_bot_second_step_next_step_url'
    ),
    path(
        'createBot/thirdStep/<str:token>/downloadConfig/',
        Download.config,
        name='download_config_url'
    ),
    path(
        'createBot/thirdStep/<str:token>/downloadScript/',
        Download.script,
        name='download_script_url'
    ),
    path(
        'deleteBot/<int:bot_id>/<str:token>/',
        DeleteBot.as_view(),
        name='delete_bot_url'
    ),
    path(
        'createBot/thirdStep/<str:token>/autoDeploy',
        RunBot.as_view(),
        name='auto_deploy_url'
    ),
    path(
        'createBot/secondStep/<str:token>/templates/',
        ShowTemplates.as_view(),
        name='templates'
    ),
    path(
        'stopBot/<str:token>/',
        StopBot.as_view(),
        name='stop_bot_url'
    ),
    path(
        'startBot/<str:token>',
        StartBot.as_view(),
        name='start_bot_url'
    ),
    path(
        'createBot/secondStep/<str:token>/callbackAnswer/',
        CreateCallbackField.as_view(),
        name='create_callback_url'
    ),
    path(
        'createBot/secondStep/<str:token>/callbackAnswer/update/',
        UpdateCallbackField.as_view(),
        name='update_callback_url'
    ),
    path(
        'createBot/secondStep/<str:token>/callbackAnswer/delete/',
        DeleteCallbackField.as_view(),
        name='delete_callback_url'
    ),
    path(
        'untilFirstStep/',
        UntilFirstStep.as_view(),
        name='until_first_step'
    ),
    path(
        'preloadingPage/',
        loading_page,
        name='loading'
    ),
    path(
        'botLogs/<str:token>/',
        BotLogs.as_view(),
        name='logs'
    ),
    path(
        'downloadLogs/<str:token>/',
        Download.download_log,
        name='download_log_url'
    )
]
