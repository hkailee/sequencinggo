from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import IntegrityError


class Profile(models.Model):
    STATUS_CHOICES = (
        ('scientist', 'Scientist'),
        ('bioinformatician', 'Bioinformatician'),
        ('clinician', 'Clinician'),
        ('justlovecontribute', 'JustLoveContributing')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/2016/09/19/default_profile.png')
    role = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scientist')
    organization = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


# Add following field to User dynamically
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
