import hashlib
from typing import List, Tuple

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from web_sound_bank.models import Sound, User, SoundRank, UserLoginToken


class UserNotFoundException(Exception):
    pass


class SoundNotFoundException(Exception):
    pass


class SoundBank:
    def get_create_or_update_user(self, user_id, username, first_name, last_name) -> User:
        user, _ = User.objects.update_or_create(_id=user_id, _username=username, _first_name=first_name,
                                                _last_name=last_name)
        return user

    def user_from_id(self, user_id) -> User:
        try:
            return User.objects.get(_id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundException

    def user_from_token(self, token) -> Tuple[User, bool]:
        try:
            user_login_token = UserLoginToken.objects.get(_token=token)
            return user_login_token.user(), user_login_token.has_expired()
        except UserLoginToken.DoesNotExist:
            raise UserNotFoundException

    def token_for_user(self, user: User) -> str:
        user_login_token = UserLoginToken.for_user(user=user)
        user_login_token.set_token_and_expiration()
        user_login_token.save()
        return user_login_token.token()

    def sound_from_id(self, sound_id) -> Sound:
        try:
            return Sound.objects.get(_id=sound_id)
        except Sound.DoesNotExist:
            raise SoundNotFoundException

    def sounds_for_user(self, user: User, query='') -> List[Sound]:
        approved_or_uploaded_sounds = Q(_is_approved=True) | Q(_uploader=user)
        query_matches_sound = Q(_title__icontains=query) | Q(_tags__icontains=query)
        qualified_sounds_filter = Q(approved_or_uploaded_sounds & query_matches_sound)

        all_qualified_sounds = Sound.objects.filter(qualified_sounds_filter)
        ranked_all_sounds = all_qualified_sounds.annotate(count=Coalesce(Sum('_rank___count'), 0)).order_by('-count')

        listened_sounds = Sound.objects.filter(_rank___user=user)
        ranked_listened_sounds = listened_sounds.annotate(count=Coalesce(Sum('_rank___count'), 0)).order_by('-count')

        return list(ranked_listened_sounds) + [sound for sound in ranked_all_sounds if sound not in ranked_listened_sounds]

    def user_listened_sound(self, user: User, sound: Sound) -> None:
        sound_rank, _ = SoundRank.objects.get_or_create(_user=user, _sound=sound)
        sound_rank.inc_count()
        sound_rank.save()

    def user_add_sound(self, user: User, title, tags, binary_data, upload_datetime) -> Sound:
        sound_id = hashlib.sha3_256(binary_data + user.user_id().encode('utf-8')).hexdigest()
        return Sound.objects.create(_id=sound_id, _title=title, _tags=tags, _bin=binary_data,
                                    _upload_datetime=upload_datetime, _uploader=user)
