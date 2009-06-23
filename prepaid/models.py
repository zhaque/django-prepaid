import datetime

from django.conf import settings
from django.contrib import auth
from django.db import models

class ValidUnitPackManager(models.Manager):
    def get_query_set(self):
        return super(ValidUnitPackManager, self).get_query_set().filter(
            expires__gt=datetime.date.today(), quantity__gt=0)

def _default_expires():
    if hasattr(settings,'PREPAID_DEFAULT_EXPIRY_PERIOD'):
        return datetime.date.today() + datetime.timedelta(
            settings.PREPAID_DEFAULT_EXPIRY_PERIOD)

class UnitPack(models.Model):
    # Normally we only deal with not expired and not empty unit packs,
    # but sometimes we need to peek into expired.
    all_objects = models.Manager()
    objects = ValidUnitPackManager()

    user = models.ForeignKey(auth.models.User)
    quantity = models.IntegerField()
    expires = models.DateField(default=_default_expires)

    # bookkeeping
    timestamp = models.DateTimeField(auto_now_add=True)
    initial_quantity = models.IntegerField()

    class Meta:
        ordering = ('expires',)

    def is_valid(self):
        return self.quantity>0 and self.expires>datetime.date.today()
    is_valid.boolean = True

    @classmethod
    def get_user_packs(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def get_user_credits(cls, user):
        return sum(up.quantity for up in cls.get_user_packs(user))

    @classmethod
    def consume(cls, user, quantity=1):
        ups = cls.get_user_packs(user)
        if sum(up.quantity for up in ups) < quantity:
            raise ValueError("User does not have enough units.")
        for up in ups:
            if up.quantity >= quantity:
                up.quantity -= quantity
                up.save()
                return
            quantity -= up.quantity
            up.quantity = 0
            up.save()

# provide default value for initial_quantity
def _handle_post_init(sender, instance=None, **kwargs):
    assert instance is not None
    if instance.initial_quantity is None:
        instance.initial_quantity = instance.quantity
models.signals.post_init.connect(_handle_post_init, sender=UnitPack)
