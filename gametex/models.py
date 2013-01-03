# coding=utf-8
"""
GameTeX models.
"""

from django.db import models
from django.contrib.auth.models import User

class GameTeXClass(models.Model):
    """
    A single GameTeX class in the GameTeX type system.  Many-to-many with GTO.
    Non-hierarchical.
    """
    name = models.CharField(max_length=256, unique=True, primary_key=True)

    def __unicode__(self):
        return self.name

class GameTeXField(models.Model):
    """
    A single defined field (e.g. "password" or "Combat Rating").
    """
    name = models.CharField(max_length=256, unique=True, primary_key=True)

    def __unicode__(self):
        return self.name

class GameTeXFieldValue(models.Model):
    """
    Mapping GameTeXObjects to GameTeXFields with specific values.
    It's how freeform values are stored in a relational database.
    """
    field = models.ForeignKey('GameTeXField')
    object = models.ForeignKey('GameTeXObject')
    value = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return "%s %s:%s" % (self.object, self.field, self.value)

class GameTeXObject(models.Model):
    """
    The heart of the system.  Each GameTeX entity
    (sheet, character, GM, keycard, whatever)
    generated by the JSON export gets its own GameTeXObject.
    """
    macro = models.CharField(max_length=256, unique=True, primary_key=True)
    name = models.CharField(max_length=256)
    classes = models.ManyToManyField(GameTeXClass)
    custom_fields = models.ManyToManyField(GameTeXField,
                                          through=GameTeXFieldValue)

    def __unicode__(self):
        return "%s [%s]" % (self.macro, self.name)

    def __getattr__(self, item):
        """
        Allows access to custom fields through dot syntax
        e.g. gto.market
        """
        return self.field(item)

    def __setattr__(self, key, value):
        """
        Allows setting custom fields.
        """
        try:
            self.set_field(key, value)
        except AttributeError:
            return super(GameTeXObject, self).__setattr__(key, value)

    def has_field(self, field):
        """
        Shortcut.  Check whether a field exists.
        """
        return GameTeXFieldValue.objects.filter(object=self,
                                                field=field).exists()

    def field(self, item):
        """
        Access a field by name.
        Useful if it contains spaces ("Combat Rating")
        """
        flds = GameTeXField.objects.filter(name=item)
        if flds.exists():
            vals = GameTeXFieldValue.objects.filter(field=flds[0],
                                                    object=self)
            if vals.exists():
                return vals[0].value
        raise AttributeError

    def set_field(self, key, value):
        """
        Set a field by name.
        """
        try:
            fieldval = GameTeXFieldValue.objects.get(field__name=key,
                                                    object=self)
            fieldval.value = value
            fieldval.save()
        except:
            raise AttributeError

    @classmethod
    def bc(cls, clname):
        """
        Get GTOs by GameTeX class (e.g. 'PC' or 'Item')
        """
        return GameTeXObject.objects.filter(classes__name=clname)


class GameTeXUser(models.Model):
    """
    Mapping between Django auth users and GameTeX PCs.
    """
    gto = models.ForeignKey('GameTeXObject')
    user = models.ForeignKey(User)

# shortcut
GTO = GameTeXObject
