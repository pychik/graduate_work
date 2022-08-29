import uuid

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField


class Stages(models.TextChoices):
    new = ('new', 'new')
    # done = ('done', 'done')
    failed = ('failed', 'failed')
    success = ('success', 'success')


class NotificationTypes(models.TextChoices):
    like = ('like', 'like')
    mass_mail = ('mass_mail', 'mass_mail')


class NotificationLogNewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stage=Stages.new).exclude(locked=True)


class NotificationLog(models.Model):
    """
    Класс логов уведомления
    """

    # STAGE_NEW = 'new'
    # STAGE_IN_WORK = 'in_work'
    # STAGE_DONE = 'done'
    #
    # STASUSES = (
    #     (STAGE_NEW, 'Новый'),
    #     (STAGE_IN_WORK, 'В работе'),
    #     (STAGE_DONE, 'Отправка завершена')
    # )

    # template_id = models.ForeignKey('template', on_delete=models.SET_NULL, related_name='notifications' )
    notification_data = JSONField(encoder=DjangoJSONEncoder, blank=True, default=dict)
    guid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status =
    locked = models.BooleanField(default=False, null=True, blank=True)
    stage = models.CharField('type',
                             max_length=20,
                             choices=Stages.choices,
                             default=Stages.new, blank=True)
    stages_data = JSONField(encoder=DjangoJSONEncoder, blank=True, default=dict)
    type = models.CharField('type',
                            max_length=20,
                            choices=NotificationTypes.choices,
                            default='', blank=True)

    # managers
    objects = models.Manager()
    new = NotificationLogNewManager()

    def __str__(self):
        return f'{self.guid}: {self.type}'

    @classmethod
    def get_object(cls, guid):
        try:
            return cls.objects.get(guid=guid)
        except cls.DoesNotExist:
            return None

    def unlock(self):
        self.locked = False
        self.save(update_fields=['locked'])
