# -*- coding: utf-8 -*-
# Copyright: Fernando Paladini <fnpaladini@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Git: https://github.com/paladini/anki-greek-letters
#
# This plugin adds greek letters to Anki Card editor.
#
# ----- Info for developers -----
#
# The method 'onAddAnkiSymbol_factory' is needed, as you can see here: 
#     http://stackoverflow.com/a/938457/2127383.
# 
# The reference for the Unicode chars is the following:
#     http://www.w3schools.com/charsets/ref_utf_greek.asp
#
from anki.hooks import wrap
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import shortcut, showInfo, showWarning, getBase, getFile, \
    openHelp, tooltip, downArrow
from BeautifulSoup import BeautifulSoup

def onAddAnkiSymbol(self, entity_number):
    my_entity = "&#" + str(entity_number) + ";"
    self.note.fields[self.currentField] += unicode(BeautifulSoup(my_entity))
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)

def onAddAnkiSymbol_factory(self, entity_number):
    return lambda s=self: onAddAnkiSymbol(self, entity_number)

def onAnkiSymbols(self):

    # Creating menus
    main = QMenu(self.mw)
    greek_capital = QMenu("Capital letters", self.mw)
    greek_small = QMenu("Small letters", self.mw)

    # Adding submenus to main menu
    main.addMenu(greek_capital)
    main.addMenu(greek_small)

    # Adding capital greek letters to submenu
    # Unicode for greek capital letters goes from 913 to 939 (including this last one).
    for capital in range(913, 940):
        a = greek_capital.addAction(unichr(capital))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, capital))

    # Adding small greek letters to submenu
    # Unicode for greek small letters goes from 940 to 974 (including this last one).
    for small in range(940, 975):
        a = greek_small.addAction(unichr(small))
        a.connect(a, SIGNAL("triggered()"), onAddAnkiSymbol_factory(self, small))

    # Adding greek symbols to submenu
    main.exec_(QCursor.pos())

def mySetupButtons(self):
    but = self._addButton("mybutton", lambda s=self: onAnkiSymbols(self),
                    text="Greek Letters " + downArrow(), size=False)

Editor.setupButtons = wrap(Editor.setupButtons, mySetupButtons)