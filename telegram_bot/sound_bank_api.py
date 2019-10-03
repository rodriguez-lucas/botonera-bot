class AbstractSoundBankAPI:
    def user_from_telegram_user(self, telegram_user):
        raise NotImplementedError()

    def sounds_for_user(self, user, sound_query):
        raise NotImplementedError()

    def static_url_for_sound(self, sound):
        raise NotImplementedError()

    def user_has_selected_sound_by_id(self, user, sound_id):
        raise NotImplementedError()
