import re

from nltk.corpus import wordnet

from PyDict.PyDictionary.util import get_object
import translators as ts


class Pydict(object):
    def __init__(self, term):
        try:
            if isinstance(term, str):
                self.term = term
            else:
                self.term = term
        except:
            self.term = term

    def meaning(self, disable_errors=False):
        if 1 < len(self.term.split()):
            print("Error: A Term must be only a single word")
        else:
            try:
                html = get_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
                    self.term))
                types = html.findAll("h3")
                lists = html.findAll("ul")
                out = {}
                for a in types:
                    reg = str(lists[types.index(a)])
                    meanings = []
                    for x in re.findall(r'\((.*?)\)', reg):
                        if 'often followed by' in x:
                            pass
                        elif len(x) > 5 or ' ' in str(x):
                            meanings.append(x)
                    name = a.text
                    out[name] = meanings
                return out
            except Exception as e:
                if not disable_errors:
                    print("Error: The Following Error occured: %s" % e)

    def translate(self, to_language):
        try:
            gs = ts
            word = gs.google(query_text=self.term, to_language=to_language)
            return word
        except:
            print("Invalid Word Or Sentence")

    def getSynonyms(self):
        synonyms = []
        for syn in wordnet.synsets(self.term):
            for i in syn.lemmas():
                synonyms.append(i.name())
        return synonyms

    def getAntonyms(self):
        antonyms = []
        for syn in wordnet.synsets(self.term):
            for i in syn.lemmas():
                if i.antonyms():
                    antonyms.append(i.antonyms()[0].name())
        return antonyms
