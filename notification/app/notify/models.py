import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField


class NotificationStages(models.TextChoices):
    new = ('new', 'new')
    failed = ('failed', 'failed')
    success = ('success', 'success')


class NotificationTypes(models.TextChoices):
    like = ('like', 'like')
    mass_mail = ('mass_mail', 'mass_mail')
    welcome = ('welcome', 'welcome')
    new_movie = ('new_movie', 'new_movie')
    delayed = ('delayed', 'delayed')
    birthday = ('birthday', 'birthday')


class NotificationLogNewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stage=NotificationStages.new).exclude(locked=True)


class NotificationLog(models.Model):
    """
    Класс логов уведомления
    """

    notification_data = JSONField(encoder=DjangoJSONEncoder, blank=True, default=dict)
    guid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    locked = models.BooleanField(default=False, null=True, blank=True)
    stage = models.CharField('Stage',
                             max_length=20,
                             choices=NotificationStages.choices,
                             default=NotificationStages.new, blank=True)
    stages_data = JSONField(encoder=DjangoJSONEncoder, blank=True, default=dict)
    notification_type = models.CharField('notification_type',
                                         max_length=20,
                                         choices=NotificationTypes.choices,
                                         default='', blank=True)
    send_tries = models.IntegerField(default=0)

    # managers
    objects = models.Manager()
    new = NotificationLogNewManager()

    def __str__(self):
        return f'{self.guid}: {self.notification_type}'

    @classmethod
    def get_object(cls, guid):
        try:
            return cls.objects.get(guid=guid)
        except cls.DoesNotExist:
            return None

    def unlock(self):
        self.locked = False
        self.save(update_fields=['locked'])

    @classmethod
    def create_by_type(cls, nl_type, data):
        values = dict(notification_type=nl_type, notification_data=data)
        return cls.objects.create(**values)

    def change_stage(self, new_stage, save=True):
        self.stage = new_stage
        if save:
            self.save(update_fields=['stage'])

    def log_error(self, error):
        if not self.stages_data.get('error'):
            self.stages_data['error'] = []
            self.stages_data['error'].append(str(error))
        self.save()

    def log_success(self, message, save=True):
        if not self.stages_data.get('success'):
            self.stages_data['success'] = []
            self.stages_data['success'].append(str(message))
        if save:
            self.save()
