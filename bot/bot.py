import logging
from uuid import uuid4

from telegram import InlineQueryResultVoice
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class BotoneraBot:
    def __init__(self, bot_token, sound_bank):
        self._updater = Updater(bot_token, use_context=True)
        self._sound_bank = sound_bank
        self._dispatcher = self._updater.dispatcher
        self._set_handlers()

    def run(self):
        self._updater.start_polling()
        self._updater.idle()

    def _set_handlers(self):
        self._dispatcher.add_handler(CommandHandler("start", self._start_command_handler))
        self._dispatcher.add_handler(CommandHandler("stop", self._stop_command_handler))

        self._dispatcher.add_handler(InlineQueryHandler(self._inlinequery_handler))
        self._dispatcher.add_error_handler(self._error_handler)

    def _start_command_handler(self, update, context):
        update.message.reply_text('Hi!')

    def _stop_command_handler(self, update, context):
        update.message.reply_text('Goodbye!')

    def _inlinequery_handler(self, update, context):
        query = update.inline_query.query

        if query is '':
            print('returning')
            return

        # todo el resultado de link que termine con el nombre y tiene que ser mp3 para que se use bien
        results = [
            InlineQueryResultVoice(id=uuid4(),
                                   voice_url='http://instantsfun.es/wp-content/uploads/2017/09/sad-trombone.mp3',
                                   title='trombone')
        ]

        update.inline_query.answer(results)

    def _error_handler(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)
