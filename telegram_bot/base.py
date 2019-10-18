import logging
from telegram import InlineQueryResultVoice
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class BotoneraBot:
    MAX_NUMBER_OF_SOUNDS_TO_SHOW = 50

    def __init__(self, bot_token, sound_bank_api):
        self._sound_bank_api = sound_bank_api
        self._updater = Updater(bot_token, use_context=True)
        self._dispatcher = self._updater.dispatcher
        self._set_handlers()

    def run(self):
        logger.info('Starting bot')
        self._updater.start_polling()
        self._updater.idle(stop_signals=[])

    def _set_handlers(self):
        self._dispatcher.add_handler(CommandHandler("start", self._start_command_handler))
        self._dispatcher.add_handler(CommandHandler("stop", self._stop_command_handler))

        self._dispatcher.add_handler(InlineQueryHandler(self._inlinequery_handler))
        self._dispatcher.add_handler(ChosenInlineResultHandler(self._chosen_inline_query_result))

        self._dispatcher.add_error_handler(self._error_handler)

    def _start_command_handler(self, update, context):
        update.message.reply_text('Hi!')

    def _stop_command_handler(self, update, context):
        update.message.reply_text('Goodbye!')

    def _inlinequery_handler(self, update, context):
        telegram_user = update.effective_user
        query_sound = update.inline_query.query

        sound_bank_user = self._sound_bank_api.user_from_telegram_user(telegram_user=telegram_user)
        sounds = self._sound_bank_api.sounds_for_user(user=sound_bank_user, query=query_sound)

        results = [
            InlineQueryResultVoice(id=sound.uuid(), voice_url=self._sound_bank_api.static_url_for_sound(sound=sound),
                                   title=sound.title()) for sound in sounds
        ]

        update.inline_query.answer(results[:self.MAX_NUMBER_OF_SOUNDS_TO_SHOW])

    def _chosen_inline_query_result(self, update, context):
        result = update.chosen_inline_result
        sound_bank_user = self._sound_bank_api.user_from_telegram_user(telegram_user=result.from_user)
        self._sound_bank_api.user_has_selected_sound_by_id(user=sound_bank_user, sound_id=result.result_id)

    def _error_handler(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)
