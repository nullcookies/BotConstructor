from django.urls import path

from .views import *

urlpatterns = [
    path('yourBots/', ShowBots.as_view(), name='show_bots_url'),
    path('createBot/', CreateBot.as_view(), name='create_bot_url'),
    path('createBot/firstStep/', CreateBotStepOne.as_view(),
         name='create_bot_first_step_url'),
    path('createBot/thirdStep/', CreateBotStepThree.as_view(),
         name='create_bot_third_step_url'),
    path('createBot/thirdStep/downloadConfig/',
         Download.config, name='download_config_url'),
    path('createBot/thirdStep/downloadScript/',
         Download.script, name='download_script_url'),
    path('updateBot/<int:bot_id>/', UpdateBot.as_view(), name='update_bot_url'),
    path('deleteBot/<int:bot_id>/', DeleteBot.as_view(), name='delete_bot_url'),
    path('createBot', CreateFileBot.as_view(), name='create_bot_file_url')
]
