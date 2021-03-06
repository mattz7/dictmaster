# -*- coding: utf-8 -*-

import re
import os
import sys

from pyquery import PyQuery as pq
from lxml import etree

from dictmaster.util import html_container_filter, words_to_db
from dictmaster.pthread import PluginThread
from dictmaster.fetcher import Fetcher
from dictmaster.postprocessor import HtmlContainerProcessor
from dictmaster.editor import Editor

# TODO: get full word list
# TODO: add index of indoeurop. roots: https://www.ahdictionary.com/word/indoeurop.html

class Plugin(PluginThread):
    def __init__(self, popts, dirname):
        if len(popts) == 0 or not os.path.exists(popts[0]):
            sys.exit("Provide full path to (existing) word list file!")
        self.word_file = popts[0]
        super(Plugin, self).__init__(popts, dirname)
        self.dictname = u"The American Heritage Dictionary of the English Language, Fifth Edition"
        self._stages = [
            AhdictFetcher(self, threadcnt=12),
            AhdictProcessor("td", self),
            Editor(plugin=self)
        ]

    def post_setup(self, cursor):
        words_to_db(self.word_file, cursor, ("utf-8", "utf-8"))

class AhdictFetcher(Fetcher):
    class FetcherThread(Fetcher.FetcherThread):
        def filter_data(self, data):
            if data == None or len(data) < 2 \
            or '<div id="results">' not in data \
            or '<div id="results">No word definition found</div>' in data:
                return None
            repl = [
                ["<!--end-->",""],
                # pronunciation
                ["","′"],
                ["","o͞o"],
                ["","ᴋʜ"] # AH uses ᴋʜ for x in IPA
            ]
            for r in repl: data = data.replace(r[0], r[1])
            regex = [
                [r'<div align="right">[^<]*<a[^>]*>[^<]*</a><script[^>]*>[^<]*</script></div>',""],
                [r'<div class="figure"><font[^>]*>[^<]*</font></div>',""],
                [r'<(img|a)[^>]*/>',""],
                [r'<a[^>]*(authorName=|indoeurop.html|\.wav")[^>]*>([^<]*)</a>',r"\2"],
                [r'<hr[^>]*><span class="copyright">[^<]*<br/>[^<]*</span>',""],
                [r'<(a|span)[^>]*>([ \n]*)</(span|a)>',r"\2"],
                [r' (name|target|title|border|cellspacing)="[^"]*"',r""],
                [r'<table width="100%">',"<table>"],
                [r"</?font[^>]*>",""],
                [r"([^ ])<(b|i|div)",r"\1 <\2"],
                [r"(b|i|div)>([^ ])",r"\1> \2"]
            ]
            for r in regex: data = re.sub(r[0], r[1], data)
            parser = etree.HTMLParser(encoding="utf-8")
            doc = pq(etree.fromstring(data, parser=parser))
            return doc("#results").html()

        def parse_uri(self, uri):
            return "https://ahdictionary.com/word/search.html?q=%s"%uri

class AhdictProcessor(HtmlContainerProcessor):
    def do_html_term(self, doc):
        term = doc("b").eq(0).text().strip()
        regex = [
            [r"\xb7",""], # the centered dot
            [r" ([0-9]+)$",r"(\1)"]
        ]
        for r in regex: term = re.sub(r[0], r[1], term)
        return term

    def do_html_definition(self, html, term):
        doc = pq(html)
        for a in doc("a:not([href])"): doc(a).replaceWith(doc(a).html())
        for a in doc("a"):
            if doc(a).text().strip() == "": doc(a).replaceWith(doc(a).text())
            elif "search.html" not in doc(a).attr("href"):
                doc(a).replaceWith(doc(a).html())
            else:
                href = "bword://%s" % doc(a).text().strip(". ").lower()
                doc(a).attr("href", href)
        doc("div.rtseg b").css("color","#069")
        doc("i").css("color","#940")
        doc("div.pseg > i").css("color","#900")
        doc("div.runseg > i").css("color","#900")
        for div in doc("div.ds-list"):
            doc(div).replaceWith(doc("<p/>").html(doc(div).html()).outerHtml())
        for div in doc("div.sds-list"): doc(div).replaceWith(doc(div).html())
        for span in doc("span"): doc(span).replaceWith(doc(span).html())
        doc("*").removeAttr("class")
        return doc.html().strip()

