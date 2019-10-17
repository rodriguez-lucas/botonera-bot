from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from sound_bank.commands import SoundFromUUIDCommand, LastAddedSoundCommand

class GetSound(View):
    def get(self, request, uuid, title):
        result = SoundFromUUIDCommand(uuid=uuid).execute()

        if result.has_errors():
            return HttpResponseNotFound(result.errors_as_str())

        sound = result.get_object()
        return HttpResponse(sound.binary_data(), content_type='audio/*')

        # response = HttpResponse()
        # response.write(sound.binary_data())
        # response['Content-Type'] = 'audio'
        # return response


class SoundsList(View):
    def head(self, *args, **kwargs):
        last_sound = LastAddedSoundCommand().execute().get_object()
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_sound.upload_datetime().strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    def get(self, *args, **kwargs):
        # todo
        pass
