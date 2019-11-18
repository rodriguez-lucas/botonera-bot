from typing import List


class RemoteSound:
    def __init__(self, sound_id, title, url):
        self._sound_id = sound_id
        self._title = title
        self._url = url

    def sound_id(self):
        return self._sound_id

    def title(self):
        return self._title

    def url(self):
        return self._url


class AbstractSoundBank:
    def create_user_if_it_does_not_exist(self, user_id, username, first_name, last_name) -> None:
        raise NotImplementedError()

    def sounds_for_user(self, user_id, sound_query) -> List[RemoteSound]:
        raise NotImplementedError()

    def user_has_selected_sound(self, user_id, sound_id) -> None:
        raise NotImplementedError()

    def login_link_for_user(self, user_id) -> str:
        raise NotImplementedError()
