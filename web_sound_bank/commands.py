from web_sound_bank.command.base import Result, Command
from web_sound_bank.sound_bank import SoundBank, SoundNotFoundException, UserNotFoundException


class CreateUserIfItDoesNotExistCommand(Command):
    def __init__(self, user_id, username, first_name, last_name):
        self._user_id = user_id
        self._username = username
        self._first_name = first_name
        self._last_name = last_name

    def execute(self):
        result = Result()
        user = SoundBank().get_create_or_update_user(user_id=self._user_id, username=self._username,
                                                     first_name=self._first_name, last_name=self._last_name)
        result.set_object(user)
        return result


class UserFromIdCommand(Command):
    def __init__(self, user_id):
        self._user_id = user_id

    def execute(self):
        result = Result()

        try:
            user = SoundBank().user_from_id(user_id=self._user_id)
            result.set_object(user)
        except UserNotFoundException:
            result.add_error("User not found")

        return result


class SoundFromIdCommand(Command):
    def __init__(self, sound_id):
        self._sound_id = sound_id

    def execute(self):
        result = Result()

        try:
            sound = SoundBank().sound_from_id(sound_id=self._sound_id)
            result.set_object(sound)
        except SoundNotFoundException:
            result.add_error("Sound not found")

        return result


class UserListenedSoundCommand(Command):
    def __init__(self, user, sound):
        self._user = user
        self._sound = sound

    def execute(self):
        SoundBank().user_listened_sound(user=self._user, sound=self._sound)
        return Result()


class SoundsForUserCommand(Command):
    def __init__(self, user, query=''):
        self._user = user
        self._query = query

    def execute(self):
        result = Result()

        sounds = SoundBank().sounds_for_user(user=self._user, query=self._query)
        result.set_object(sounds)

        return result


class LoginTokenForUserCommand(Command):
    def __init__(self, user):
        self._user = user

    def execute(self):
        result = Result()

        token = SoundBank().token_for_user(user=self._user)
        result.set_object(token)

        return result


class LoginUserFromTokenCommand(Command):
    def __init__(self, token, request):
        self._token = token
        self._request = request

    def execute(self):
        result = Result()

        try:
            user, token_has_expired = SoundBank().user_from_token(token=self._token)
            SoundBank().delete_token_for_user(user=user)
            if token_has_expired:
                result.add_error("Token has expired")
            else:
                two_hours = 60 * 60 * 2
                self._request.session.set_expiry(two_hours)
                self._request.session['user_id'] = user.user_id()
                result.set_object(user)
        except UserNotFoundException:
            result.add_error("User not found")

        return result


class LogoutUserCommand(Command):
    def __init__(self, user, request):
        self._user = user
        self._request = request

    def execute(self):
        SoundBank().delete_token_for_user(user=self._user)
        del self._request.session['user_id']
        return Result()


class UserIsLoggedInCommand(Command):
    def __init__(self, request):
        self._request = request

    def execute(self):
        result = Result()
        result.set_object('user_id' in self._request.session)
        return result


class LoggedInUserCommand(Command):
    def __init__(self, request):
        self._request = request

    def execute(self):
        result = Result()
        result.set_object(UserFromIdCommand(user_id=self._request.session['user_id']).execute().get_object())
        return result


class AddSoundCommand(Command):
    def execute(self):
        # todo add sound to database
        pass

