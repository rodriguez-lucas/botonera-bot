import logging
from django.core.management.base import BaseCommand
from telegram_bot.base import BotoneraBot
from telegram_bot.sound_bank_api import AbstractSoundBankAPI
from settings import BOT_TOKEN, GET_SOUND_URL
from sound_bank.base import SoundBank, SoundBankException


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class SoundBankAPI(AbstractSoundBankAPI):
    def sounds_for_user(self, user, query):
        return self._sound_bank().sounds_for_user(user=user, query=query)

    def user_has_selected_sound_by_id(self, user, sound_id):
        try:
            sound = self._sound_bank().sound_from_uuid(sound_id)
            self._sound_bank().user_listened_sound(user=user, sound=sound)
        except SoundBankException as e:
            logger.info('Exception: {exception} - User: {user} - sound_id: {sound_id}'.format(exception=e, user=user,
                                                                                              sound_id=sound_id))

    def static_url_for_sound(self, sound):
        sound_title = ''.join([i if ord(i) < 128 else '' for i in sound.title()]).replace(' ', '_')
        return '{base_url}/{sound_uuid}/{sound_title}'.format(base_url=GET_SOUND_URL,
                                                              sound_uuid=sound.uuid(),
                                                              sound_title=sound_title)

    def user_from_telegram_user(self, telegram_user):
        return self._sound_bank().register_or_get_user(user_id=telegram_user['id'],
                                                       username=telegram_user['username'],
                                                       first_name=telegram_user['first_name'],
                                                       last_name=telegram_user['last_name'])

    def _sound_bank(self) -> SoundBank:
        return SoundBank()


class Command(BaseCommand):
    help = 'Run telegram bot: BotoneraBot with sound_bank'

    def handle(self, *args, **options):
        BotoneraBot(bot_token=BOT_TOKEN, sound_bank_api=SoundBankAPI()).run()
