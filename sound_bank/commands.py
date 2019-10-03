from command.base import Result, Command
from sound_bank.base import SoundBank, SoundBankException


class SoundFromUUIDCommand(Command):
    def __init__(self, uuid):
        self._uuid = uuid

    def execute(self):
        result = Result()

        try:
            sound = SoundBank().sound_from_uuid(uuid=self._uuid)
            result.set_object(sound)
        except SoundBankException:
            result.add_error("Sound not found")

        return result


class LastAddedSoundCommand(Command):
    def execute(self):
        result = Result()

        try:
            result.set_object(SoundBank().last_added_sound())
        except SoundBankException:
            result.add_error("Can't return last added sound")

        return result


class SoundsForUserCommand(Command):
    def execute(self):
        pass


class AddSoundCommand(Command):
    def execute(self):
        # todo add sound to database
        pass


class UserSentSoundCommand(Command):
    def execute(self):
        # todo update sound rank
        pass

