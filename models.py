from django.db import models

# Create your models here.

class GameTeXClass(models.Model):
    name = models.CharField(max_length=256, unique=True, primary_key=True)

    def __unicode__(self):
        return "GTO: %s" % self.name

class GameTeXField(models.Model):
    name = models.CharField(max_length=256, unique=True, primary_key=True)

    def __unicode__(self):
        return "GTF: %s" % self.name

class GameTeXFieldValue(models.Model):
    field = models.ForeignKey('GameTeXField')
    object = models.ForeignKey('GameTeXObject')
    value = models.CharField(max_length=256)

    def __unicode__(self):
        return "GTFV: %s %s:%s" % (self.object, self.field, self.value)

class GameTeXObject(models.Model):
    macro = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    classes = models.ManyToManyField(GameTeXClass)
    custom_fields = models.ManyToManyField(GameTeXField, through=GameTeXFieldValue)

    def __unicode__(self):
        return "GTO: %s [%s]" % (self.macro, self.name)

    def __getattr__(self, item):
        """
        Allows access to custom fields through dot syntax
        e.g.
        """
        return self.field(item)

    def __setattr__(self, key, value):
        try:
            self.set_field(key, value)
        except AttributeError:
            return super(GameTeXObject, self).__setattr__(key, value)

    def field(self, item):
        flds = GameTeXField.objects.filter(name=item)
        if len(flds):
            vals = GameTeXFieldValue.objects.filter(field=flds[0],object=self)
            if len(vals):
                return vals[0].value
        raise AttributeError

    def set_field(self, key, value):
        try:
            v = GameTeXFieldValue.objects.get(field__name=key,object=self)
            v.value = value
            v.save()
        except:
            raise AttributeError

    @classmethod
    def bc(cls, clname):
        return GameTeXObject.objects.filter(classes__name=clname)


# shortcut
GTO = GameTeXObject