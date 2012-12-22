gametex-django
==============

Getting started
---------------

A Django app for GameTeX integration (beta).  Provides trivial integration with GameTeX classes.

To install:

* Either clone the gametex-django repo where your Django apps live, or add it as a submodule.
  Example: 'git submodule add https://github.com/ternus/gametex-django.git gametex'
* Add 'gametex' to your INSTALLED_APPS in settings.py.
* Create a local_settings.py file in the gametex/ folder (there's an example) that sets JSON_PRINT_FILENAME to the location of your game's json-PRINT.json file.

To import your game data:

* You can use django_extensions' 'runscript' feature:
  ./manage.py runscript --pythonpath=. gametex.import 

You then have access to everything exported in your JSON file, all within Django.

Django model mapping
--------------------

Each GameTeX entity (sheet, ability, PC, etc.) becomes a GameTeXObject
(GTO for short).  Each GTO belongs to a number of classes, such as
'KeyCard', 'Item', or 'PC'; a 'PC' might also be a 'Char'.  (There's
no hierarchical representation in the GameTeX Django models.)

There's a shortcut method, 'bc', that allows you to filter
GameTeXObjects by class.

Each GTO has a 'name', a 'number', and a 'macro'; some of these may be
blank.  You can query using any of these, and you can access them in
the usual way:

    >>> g = GTO.bc('PC')[0]
    >>> g.name
    u'Captain GameTeX'	
    >>> g.macro
    u'cTest'
    >>> g.number
    u'22234'

Note that 'number' is a text field by default and thus returns a
string.

GTOs may also have custom fields defined, depending on how your game
looks.  For example, an item might have a 'price' field.  You can
access these like normal:

    >>> g2 = GTO.bc('KeyCard')[0]
    >>> g2.name
    u'CompSci Data'
    >>> g2.hintreq
    u'Cryptography 2'

In case your field has spaces in it, you can reference it with the
'field' method of GameTeXObject:

    >>> g.field('Combat Rating')
    u'2'
