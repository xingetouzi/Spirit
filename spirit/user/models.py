# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import timedelta
import os

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from ..core.conf import settings
from ..core.utils.models import AutoSlugField


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))

        return name


def upload_article_cover(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(instance.user.id), ext)
    return "image/{}".format(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("profile"), related_name='st')

    slug = AutoSlugField(populate_from="user.username", db_index=False, blank=True)
    location = models.CharField(_("location"), max_length=75, blank=True)
    last_seen = models.DateTimeField(_("last seen"), auto_now=True)
    last_ip = models.GenericIPAddressField(_("last ip"), blank=True, null=True)
    timezone = models.CharField(_("time zone"), max_length=32, default='Asia/Shanghai')
    is_administrator = models.BooleanField(_('administrator status'), default=False)
    is_moderator = models.BooleanField(_('moderator status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False,
                                      help_text=_('Designates whether the user has verified his '
                                                  'account by email or by other means. Un-select this '
                                                  'to let the user activate his account.'))

    topic_count = models.PositiveIntegerField(_("topic count"), default=0)
    comment_count = models.PositiveIntegerField(_("comment count"), default=0)

    last_post_hash = models.CharField(_("last post hash"), max_length=32, blank=True)
    last_post_on = models.DateTimeField(_("last post on"), null=True, blank=True)
    image = models.ImageField(upload_to=upload_article_cover, default=u"image/default.png", max_length=100, storage=OverwriteStorage())

    class Meta:
        verbose_name = _("forum profile")
        verbose_name_plural = _("forum profiles")

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            self.is_administrator = True

        if self.is_administrator:
            self.is_moderator = True

        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('spirit:user:detail', kwargs={'pk': self.user.pk, 'slug': self.slug})

    def update_post_hash(self, post_hash):
        assert self.pk

        # Let the DB do the hash
        # comparison for atomicity
        return bool(UserProfile.objects
                    .filter(pk=self.pk)
                    .exclude(
                        last_post_hash=post_hash,
                        last_post_on__gte=timezone.now() - timedelta(
                            minutes=settings.ST_DOUBLE_POST_THRESHOLD_MINUTES))
                    .update(
                        last_post_hash=post_hash,
                        last_post_on=timezone.now()))
