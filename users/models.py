from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.



class AbstractAutoDate(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True,)
    modified = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    '''
    User model, using mobile as primary key. User with is_registered are the one registered.
    and user who are not is_registered are bieng added by someone's else contact list.
    '''
    spam_marked_count = models.IntegerField(default=0)
    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True)
    is_registered = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class Contact(AbstractAutoDate, models.Model):
    primary_contact = models.ForeignKey(
        User, related_name='primary_contact')

    related_contact = models.ForeignKey(
        User, related_name='realted_contact')


class SpamMarkedHisory(AbstractAutoDate, models.Model):

    by = models.ForeignKey(
        User, related_name='marked_by')

    to = models.ForeignKey(
        User, related_name='marked_to')


