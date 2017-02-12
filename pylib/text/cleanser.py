"""
Text cleanser
@author TaoPR (github.com/starcolon)
"""

import re

"""
Remove unwanted tokens from the given text
"""
def cleanse(txt):
  txt_ = txt
  for p in patterns():
    txt_ = re.sub(p, '', txt_)
  return txt_

def patterns():
  [r'{.+}',\
    r'<.+>',\
    r'&#.+;']

