"""
Text cleanser
@author TaoPR (github.com/starcolon)
"""

import re

"""
Remove unwanted tokens from the given text
"""
def cleanse(txt):
  return ''.join(filter(str.isalnum, txt))
#   for p in patterns():
#     txt_ = re.sub(p, ' ', txt_)
#   return txt_

# def patterns():
#   return [ \
#     r'^\-',
#     r'\"',\
#     r"\'",\
#     r'\:',\
#     r'\;',\
#     r'\#',\
#     r'\^',\
#     r'\(',\
#     r'\)',\
#     r'\,',\
#     r'\{.+\}',\
#     r'\{',\
#     r'\}',\
#     r'\\'\
#     r'\<.*\>',\
#     r'&#.+;',\
#     r'\.',\
#     r'\+',\
#     r'\!',\
#     r'\n',\
#     r'[\d+]',
#     r' \w{1,2}\.',
#     r'\[.*\]',
#     r'title=\"\w*\"']

