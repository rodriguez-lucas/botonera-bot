from django.http import HttpResponse, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views import View

from web_sound_bank.commands import SoundFromIdCommand, SoundsForUserCommand, UserFromIdCommand


class GetSound(View):
    def get(self, request, sound_id, title):
        result = SoundFromIdCommand(sound_id=sound_id).execute()

        if result.has_errors():
            return HttpResponseNotFound(result.errors_as_str())

        sound = result.get_object()
        return HttpResponse(sound.binary_data(), content_type='audio/mpeg')


class SoundsList(View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')

        user = None
        sounds = []
        user_cmd_result = UserFromIdCommand(user_id=user_id).execute()

        if not user_cmd_result.has_errors():
            user = user_cmd_result.get_object()
            sounds = SoundsForUserCommand(user=user).execute().get_object()

        context = {'user': user, 'sounds': sounds}
        response = TemplateResponse(request=request, template='sounds-list.html', context=context)
        return response
