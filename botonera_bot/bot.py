import logging

from telegram import InlineQueryResultVoice
from telegram.constants import MAX_INLINE_QUERY_RESULTS
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class BotoneraBot:
    def __init__(self, bot_token, sound_bank):
        self._sound_bank = sound_bank
        self._updater = Updater(bot_token, use_context=True)
        self._dispatcher = self._updater.dispatcher

        self._set_handlers()

    def run(self):
        logger.info('Starting bot')
        self._updater.start_polling()
        self._updater.idle()

    def _set_handlers(self):
        # Commands
        self._dispatcher.add_handler(CommandHandler("start", self._start_command_handler))
        self._dispatcher.add_handler(CommandHandler("help", self._start_command_handler))
        self._dispatcher.add_handler(CommandHandler("login", self._login_to_web_sound_bank_command_handler))

        # Inline query
        self._dispatcher.add_handler(InlineQueryHandler(self._inlinequery_handler))
        self._dispatcher.add_handler(ChosenInlineResultHandler(self._chosen_inline_query_result))

        # Error
        self._dispatcher.add_error_handler(self._error_handler)

    def _start_command_handler(self, update, context):
        update.message.reply_text('Hi! use inline query to send sounds, like this:\n@botonera_bot <SOUND QUERY>')

    def _login_to_web_sound_bank_command_handler(self, update, context):
        user_dict = update.effective_user
        self._sound_bank.create_user_if_it_does_not_exist(user_id=user_dict['id'],
                                                          username=user_dict['username'],
                                                          first_name=user_dict['first_name'],
                                                          last_name=user_dict['last_name'])

        login_link = self._sound_bank.login_link_for_user(user_id=user_dict['id'])
        update.message.reply_text('Use the following link to login and manage your sounds: {}'.format(login_link))

    def _inlinequery_handler(self, update, context):
        query_sound = update.inline_query.query
        user_dict = update.effective_user

        self._sound_bank.create_user_if_it_does_not_exist(user_id=user_dict['id'],
                                                          username=user_dict['username'],
                                                          first_name=user_dict['first_name'],
                                                          last_name=user_dict['last_name'])

        sounds = self._sound_bank.sounds_for_user(user_id=user_dict['id'], query=query_sound)

        results = [
            InlineQueryResultVoice(id=sound.sound_id(), voice_url=sound.url(), title=sound.title()) for sound in sounds
        ]

        update.inline_query.answer(results[:MAX_INLINE_QUERY_RESULTS])

    def _chosen_inline_query_result(self, update, context):
        result = update.chosen_inline_result
        self._sound_bank.user_has_selected_sound(user_id=result.from_user['id'], sound_id=result.result_id)

    def _error_handler(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)
