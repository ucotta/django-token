import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

import binascii


@python_2_unicode_compatible
class Token(models.Model):
    """
    An access token that is associated with a user.  This is essentially the same as the token model from Django REST Framework
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="token", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
