GameTeX Django
==============

A Django app for GameTeX integration.  Writing a ten-day webapp?  You'll want this.

Getting started
---------------

You'll need a version of GameTeX that supports JSON export (talk to Ken).

To install:

* Either clone the gametex-django repo where your Django apps live, or add it as a submodule.
  Example: `git submodule add https://github.com/ternus/gametex-django.git gametex`
* Add `gametex` to your INSTALLED_APPS in settings.py.
* Run `./manage.py syncdb` to create the new models.

To import your game data:

* Generate `json_PRINT.json` by LaTeXing `json_PRINT.tex` in your game's Production directory.
* Run `./manage.py load_gametex /path/to/json-PRINT.json`

You then have access to everything exported in your JSON file, all within Django.

If you pass the `--clear` argument to `./manage.py load_gametex`,
all existing GameTeX objects will be deleted from your database.

If you pass the `--create-users` argument, *and* all your PCs have
'username' and 'password' fields, the loader will automatically create
users for each of your PCs and create GameTeXUser entries to map between
them.

Django model mapping
--------------------

Each GameTeX entity (sheet, ability, PC, etc.) becomes a GameTeXObject
(GTO for short).  Each GTO belongs to a number of classes, such as
'KeyCard', 'Item', or 'PC'; a 'PC' might also be a 'Char'.  (There's
no hierarchical representation in the GameTeX Django models; that's up
to GameTeX.)

There's a shortcut method, 'bc', that allows you to filter
GameTeXObjects by class.

Each GTO has a 'name', a 'number', and a 'macro'; 'name' and 'number'
may be blank.  You can query using any of these, and you can access
them in the usual way:

    >>> g = GTO.bc('PC')[0]
    >>> g.name
    u'Captain GameTeX'	
    >>> g.macro
    u'cTest'
    >>> g.number
    u'22234'

Note that all fields are Unicode text, even ostensibly numerical ones
such as 'number'.  It's up to you to convert those to int (or whatever)
if necessary.

GTOs may also have custom fields defined, depending on how your game
looks.  For example, an item might have a 'price' field.  You can
access these like normal:

    >>> g2 = GTO.bc('KeyCard')[0]
    >>> g2.name
    u'CompSci Data'
    >>> g2.hintreq
    u'Cryptography 2'
    >>> g2.name = 'CS Data'
    >>> g2.name
    u'CS Data'

In case your field has spaces in it, you can reference it with the
'field' and 'set_field' methods of GameTeXObject:

    >>> g.has_field('Combat Rating')
    True
    >>> g.field('Combat Rating')
    u'2'
    >>> g.set_field('Combat Rating', '4')
    >>> g.field('Combat Rating')
    u'4'

