# -*- coding: utf-8 -*-
import logging

from syntaxnet_wrapper import parser, language_code_to_model_name

# Overrides available languages map
language_code_to_model_name['en'] = 'English'  # Do not use Parsey McParseface

logging.basicConfig(level=logging.INFO)

#=================
def go(language_code, text):
    #text = u"I am a pig"
    try:
        conllu = parser[language_code].query(text, returnRaw=True)
        if conllu is None:
           logging.error('Bad SyntaxNet output')
        return conllu
    except Exception  as e:
           logging.error(repr(e))

if __name__ == '__main__':
   print( go('en', u"I am a pig") )
   print( go('zh', u"我是一隻豬") )

