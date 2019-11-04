from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

from web_sound_bank.commands import SoundFromIdCommand, SoundsForUserCommand, UserFromIdCommand, \
    LoginUserFromTokenCommand, UserIsLoggedInCommand, LoggedInUserCommand


class LoginView(View):
    def get(self, request, token):
        result = LoginUserFromTokenCommand(token=token, request=request).execute()
        if result.has_errors():
            redirect_url = reverse('login-required')
        else:
            redirect_url = reverse('home')

        return HttpResponseRedirect(redirect_url)


class GetSound(View):
    def get(self, request, sound_id, title):
        result = SoundFromIdCommand(sound_id=sound_id).execute()

        if result.has_errors():
            return HttpResponseNotFound(result.errors_as_str())

        sound = result.get_object()
        return HttpResponse(sound.binary_data(), content_type='audio/mpeg')


class LoggedInView(View):
    def dispatch(self, request, *args, **kwargs):
        user_is_logged_in = UserIsLoggedInCommand(request=request).execute().get_object()
        if not user_is_logged_in:
            return HttpResponseRedirect(reverse('login-required'))

        return super().dispatch(request, *args, **kwargs)

    def user(self):
        return LoggedInUserCommand(request=self.request).execute().get_object()


class SoundsList(LoggedInView):
    def get(self, request, *args, **kwargs):
        sounds = SoundsForUserCommand(user=self.user()).execute().get_object()

        context = {'user': self.user(), 'sounds': sounds}
        response = TemplateResponse(request=request, template='sounds-list.html', context=context)
        return response
