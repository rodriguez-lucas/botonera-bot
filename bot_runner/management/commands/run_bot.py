import logging
from threading import Thread
from time import sleep

import requests
from django.core.management.base import BaseCommand
from botonera_bot.bot import BotoneraBot
from botonera_bot.abstract_sound_bank import AbstractSoundBank, RemoteSound
from web_sound_bank.commands import UserFromIdCommand, SoundsForUserCommand, SoundFromIdCommand, \
    UserListenedSoundCommand, CreateUserIfItDoesNotExistCommand, LoginTokenForUserCommand
from web_sound_bank.settings import BOT_TOKEN, GET_SOUND_URL, LOGIN_BASE_URL, SERVER_DOMAIN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class WebSoundBank(AbstractSoundBank):
    def sounds_for_user(self, user_id, query):
        user_cmd_result = UserFromIdCommand(user_id=user_id).execute()

        if user_cmd_result.has_errors():
            logger.info('UserCommandErrors: {}'.format(user_cmd_result.errors_as_str()))
            return []

        user = user_cmd_result.get_object()
        sounds = SoundsForUserCommand(user=user, query=query).execute().get_object()
        return [
            RemoteSound(sound_id=sound.sound_id(), title=sound.title(), url=self._static_url_for_sound(sound=sound))
            for sound in sounds
        ]

    def user_has_selected_sound(self, user_id, sound_id):
        user_cmd_result = UserFromIdCommand(user_id=user_id).execute()
        sound_cmd_result = SoundFromIdCommand(sound_id=sound_id).execute()

        if user_cmd_result.has_errors() or sound_cmd_result.has_errors():
            logger.info('UserCommandErrors: {} - SoundCommandErrors: {}'.format(user_cmd_result.errors_as_str(),
                                                                                sound_cmd_result.errors_as_str()))
            return

        UserListenedSoundCommand(user=user_cmd_result.get_object(), sound=sound_cmd_result.get_object()).execute()

    def create_user_if_it_does_not_exist(self, user_id, username, first_name, last_name):
        return CreateUserIfItDoesNotExistCommand(user_id=user_id, username=username, first_name=first_name,
                                                 last_name=last_name).execute()

    def login_link_for_user(self, user_id) -> str:
        user_cmd_result = UserFromIdCommand(user_id=user_id).execute()

        if not user_cmd_result.has_errors():
            user = user_cmd_result.get_object()
            token = LoginTokenForUserCommand(user=user).execute().get_object()
            return '{base_url}/{token}'.format(base_url=LOGIN_BASE_URL, token=token)

        logger.info('UserCommandErrors: {}'.format(user_cmd_result.errors_as_str()))
        return ''

    def _static_url_for_sound(self, sound):
        sound_title = ''.join([i if ord(i) < 128 else '' for i in sound.title()]).replace(' ', '_')
        return '{base_url}/{sound_id}/{sound_title}'.format(base_url=GET_SOUND_URL,
                                                            sound_id=sound.sound_id(),
                                                            sound_title=sound_title)


class KeepAliveHerokuWebServiceHack:
    def _ping_request(self):
        response = requests.get(f'http://{SERVER_DOMAIN}/ping')
        logger.info(f'Ping: {response}')

    def run(self):
        waiting_time_in_minutes = 28
        while True:
            self._ping_request()
            sleep(waiting_time_in_minutes * 60)


class Command(BaseCommand):
    help = 'Run telegram bot: botonera_bot with web_sound_bank'

    def handle(self, *args, **options):
        # FIXME horrible hack!
        threads = [Thread(target=BotoneraBot(bot_token=BOT_TOKEN, sound_bank=WebSoundBank()).run, daemon=True),
                   Thread(target=KeepAliveHerokuWebServiceHack().run, daemon=True)]

        for thread in threads:
            thread.start()
