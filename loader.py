__author__ = 'ternus'

from models import *
import json

def import_gametex(filename):
    gametex_file = file(filename, 'r')
    gametex_json = json.load(gametex_file)
    for obj in gametex_json:
        g = GTO.objects.get_or_create(macro=obj['macro'],
                name=obj['name'])[0]
        for cls in obj['classes']:
            c = GameTeXClass.objects.get_or_create(name=cls)[0]
            g.classes.add(c)
        for field in obj:
            if field == 'macro' or field == 'name' or field == 'classes': continue
            f = GameTeXField.objects.get_or_create(name=field)[0]
            v = GameTeXFieldValue.objects.get_or_create(field=f, object=g, value=obj[field])
    print "Done."