dictmaster
======

A simple tool that automatically fetches dictionary data from
different offline and online sources.
The dictionaries are prettified and automatically converted to stardict
format.
The input format might be some XML or HTML format. Zipped
data is also supported and there is basic support for Babylon dictionaries.

Supported dictionary sources
---

At the moment you can fetch dictionary data from any Babylon dictionary (`*.bgl`) 
available on your computer.
Furthermore `dictmaster` is able to retrieve data from the following online sources:
etymonline.com, zeno.org (Georges, Pape), Dictionnaire de l'Académie Française (http://atilf.atilf.fr/academie.htm),
Folkets Lexikon (http://folkets-lexikon.csc.kth.se/folkets/) and XMLittré (littre.org).

Dictionaries that are easily accessible and might be integrated in future versions are
listed in the following blog post:

http://tovotu.de/blog/536-Kostenlose-Wrterbcher-fr-die-Offlinenutzung/

How to get started
---

All the conversion to stardict is done with the help of pyglossary
(https://github.com/ilius/pyglossary). Before you start you have
to pull in the third party code with

    git submodule update --init

Start the tool with:

    ./dictmaster.py PLUGIN_NAME
    
You find available plugins in the `plugins` directory.

Your dictionary data will be saved to `data/PLUGIN_NAME/stardict.*` in
stardict format. (Note that for some dictionaries the directory
`data/PLUGIN_NAME/res` is also needed.)

If the data has been fetched but postprocessing fails or if you want to
rerun postprocessing for whatever reason without redownloading all the data
you simply add the option `--use-raw`.

Limitations
---

Even though this projects looks pretty modularized and extendible at first
glance, let me tell you that this is unfortunately not the case - yet.
For now, you really have to go through the code and understand what's happening
in order to write new plugins.

Todo list
---

- Extendibility: Implement some kind of standard procedure for adding new plugins or at 
least provide plugin templates that you can use if you wish to add new ones.
- Usability: A graphical user interface that guides you through the process.
- A way to edit existing (ready converted) dictionary data using some kind
of user interface.

Legal issues
---

Keep in mind that you might not be the copyright holder for the data you download with
the help of dictmaster. I'm not even sure whether this kind of data aggregation itself is legal.
However, the stardict dictionaries created with dictmaster won't be freely distributable
in most cases - personal use should be okay though.