from django.urls import path

from .views import *

urlpatterns = [
    path('yourBots/', ShowBots.as_view(), name='show_bots_url'),
    path('createBot/firstStep/', CreateBotStepOne.as_view(), name='create_bot_first_step_url'),
    path('createBot/thirdStep/', CreateBotStepThree.as_view(), name='create_bot_third_step_url'),
    path('createBot/secondStep/text/', CreateBotStepTwo.text_field_create, name='create_bot_second_step_text_url'),
    path('createBot/secondStep/text/delete/<int:button_id>/', CreateBotStepTwo.text_field_delete, name='create_bot_second_step_text_delete_url'),
    path('createBot/secondStep/text/update/', CreateBotStepTwo.text_field_update, name='create_bot_second_step_text_update_url'),
    path('createBot/secondStep/replyMarkup/', CreateBotStepTwo.reply_markup_field_create, name='create_bot_second_step_reply_markup_url'),
    path('createBot/secondStep/nextStep/', CreateBotStepTwo.generate_file, name='create_bot_second_step_next_step_url'),
    path('createBot/thirdStep/downloadConfig/', Download.config, name='download_config_url'),
    path('createBot/thirdStep/downloadScript/', Download.script, name='download_script_url'),
    path('updateBot/<int:bot_id>/', UpdateBot.as_view(), name='update_bot_url'),
    path('deleteBot/<int:bot_id>/', DeleteBot.as_view(), name='delete_bot_url'),
]
