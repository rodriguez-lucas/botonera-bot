from django.core.exceptions import ValidationError

from app.models import Sound
from command.base import Result, Command


class SoundFromUUIDCommand(Command):
    def __init__(self, uuid):
        self._uuid = uuid

    def execute(self):
        result = Result()

        try:
            sound = Sound.objects.get(_uuid=self._uuid)
            result.set_object(sound)
        except(Sound.DoesNotExist, ValidationError):
            result.add_error('Sound not found')

        return result


class LastAddedSoundCommand(Command):
    def execute(self):
        result = Result()
        result.set_object(Sound.objects.order_by('-id').first())
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

