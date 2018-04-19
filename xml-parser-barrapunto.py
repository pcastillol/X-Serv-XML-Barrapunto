#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import os

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False #variable booleana que se activara cuando dentro de item.
        self.inContent = False  #variable booleana que se activara cuando contenido (characters) del elemento nos interese.
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent.encode("utf-8") + "."    # To avoid Unicode trouble
                print line
                self.title = self.theContent.encode("utf-8")
                self.inContent = False
                self.theContent = ""

            elif name == 'link':
                line = " Link: " + self.theContent + "."
                print line
                self.link = self.theContent.encode("utf-8")
                pinchable = "<a href='" + self.link + "'>" + self.title + "</a><br>"
                htmlFile.write(pinchable)
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

# Load parser and driver

theParser = make_parser()   #make_parser devuelve un XMLReader object (parseador).
theHandler = myContentHandler() #instancias la clase myContentHandler (manejador).
theParser.setContentHandler(theHandler) #al parseador le pasas el manejador.

# Ready, set, go!

xmlFile = open(sys.argv[1],"r") #abre el documento XML en modo lectura, el cual sera pasado como segundo argumento.

if os.path.exists("barrapunto.html"):
    htmlFile = open("barrapunto.html", "a")
else:
    htmlFile = open("barrapunto.html", "w")

theParser.parse(xmlFile)    #al parseador le pasas el documento XML. En esta linea se ejecuta la accion de parsear.

htmlFile.close()

print "Parse complete"
