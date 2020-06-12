
def laceStrings(s1, s2):

    """

    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,

    beginning with s1. If strings are not of same length,

    then the extra elements should appear at the end.

    """

    # Your Code Here

  def recLace(s1, s2, laceString):

    if s1 == '':

      return laceString+s2

    if s2 == '':

      return laceString+s1

    else:

      return recLace(s1[1:], s2[1:], out+s1[0]+s2[0])

  return recLace(s1, s2, '')

s1='abc'    
s2='mxy'
print (laceStrings(s1, s2))
    