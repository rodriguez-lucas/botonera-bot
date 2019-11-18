import hashlib
import time
import uuid

from django.db import models


class User(models.Model):
    _id = models.CharField(max_length=100, unique=True, primary_key=True)
    _username = models.CharField(max_length=100)
    _first_name = models.CharField(max_length=100, blank=True, null=True)
    _last_name = models.CharField(max_length=100, blank=True, null=True)

    def user_id(self):
        return self._id

    def username(self):
        return self._username

    def first_name(self):
        return self._first_name

    def last_name(self):
        return self._last_name

    def __str__(self):
        return self._username


class Sound(models.Model):
    _id = models.CharField(max_length=64, unique=True, primary_key=True)
    _title = models.CharField(max_length=100)
    _tags = models.TextField(blank=True)
    _bin = models.BinaryField()
    _upload_datetime = models.DateTimeField()
    _uploader = models.ForeignKey(User, related_name='uploaded_sounds', on_delete=models.PROTECT)

    _is_approved = models.BooleanField(default=False)

    def sound_id(self):
        return self._id

    def title(self):
        return self._title

    def formatted_title(self):
        return self._title.replace(' ', '-')

    def tags(self):
        return self._tags

    def binary_data(self):
        return bytes(self._bin)

    def is_approved(self):
        return self._is_approved

    def upload_datetime(self):
        return self._upload_datetime

    def __str__(self):
        return self._title


class SoundRank(models.Model):
    _user = models.ForeignKey(User, on_delete=models.PROTECT)
    _sound = models.ForeignKey(Sound, on_delete=models.PROTECT, related_name='_rank')
    _count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['_user', '_sound'], name='sound rank constraint')]

    def __str__(self):
        return '{} | {} | {}'.format(self._user, self._sound, self._count)

    def inc_count(self):
        self._count += 1


class UserLoginToken(models.Model):
    _user = models.OneToOneField(User, on_delete=models.PROTECT)
    _token = models.CharField(max_length=64, unique=True)
    _expiration_timestamp = models.BigIntegerField()

    @classmethod
    def for_user(cls, user):
        try:
            user_login_token = cls.objects.get(_user=user)
        except cls.DoesNotExist:
            user_login_token = cls(_user=user)

        return user_login_token

    def user(self) -> User:
        return self._user

    def token(self) -> str:
        return self._token

    def set_token_and_expiration(self, expiration=60*60*1) -> None:
        self._expiration_timestamp = int(time.time() + expiration)
        self._token = hashlib.sha3_256((uuid.uuid4().hex + self._user.user_id()).encode('utf-8')).hexdigest()

    def has_expired(self) -> bool:
        return time.time() > self._expiration_timestamp

    def __str__(self):
        return '{username}'.format(username=self.user().username())


