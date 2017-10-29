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

