""" Module defines classes Token and Tokenizer."""


import unicodedata


class Token(object):
    """ A token with its string, start, end positions and type """
    def __init__(self, s, f_ch, l_ch, typ):
        self.tok = s
        self.f_ch = f_ch
        self.l_ch = l_ch
        self.typ = typ

    def __repr__(self):
        return "%s : [%s - %s], %s" % (self.tok, self.f_ch, self.l_ch, self.typ)

    def __eq__(self, other):
        return ((self.tok == other.tok) and (self.f_ch == other.f_ch) and
                (self.l_ch == other.l_ch)and (self.typ == other.typ))


class Tokenizer(object):
    """
    Class of tokenizers.

    Method "tokenize" creates a list of token instances from a string,
    that is a substring of consecutive alphabetical symbols
    """
    def check_typ(self, s):
        """ Return the string containing the type of the symbol. """
        self.s = s
        if s.isalpha():
            return "alph"
        elif s.isspace():
            return "space"
        elif s.isdigit():
            return "digit"
        elif unicodedata.category(s).startswith("P"):
            return "punct"
        else:
            return "other"

    def alph_tokenize(self, s):
        """
        Take a string and generate alphabetical and diigital Tokens.

        """
        self.s = s
        if not isinstance(s, str):
            raise TypeError("You can only tokenize string objects!")
        f = 0  # variable for the start position of a token
        for i, x in enumerate(s):
            # start with the second symbol
            if not i == 0:
                # save the type of the previous symbol
                prevt = self.check_typ(s[i-1])
                # check for the change of type
                if prevt != self.check_typ(x):
                    l = i - 1   # set the last position for the token
                    tok = Token(s[f:l+1], f, l, prevt)
                    if prevt == "alph" or prevt == "digit":
                        yield tok
                    f = i
                    continue
                continue
        # create the token at the end of the string
        if not len(s) == 0:
            l = len(s)-1
            prevt = self.check_typ(s[len(s)-1])
            tok = Token(s[f:l+1], f, l, prevt)
            if prevt == "alph" or prevt == "digit":
                yield tok


    def i_tokenize(self, s):
        """
        Take a string and generate a list of Tokens.

        Check the type of the current and previous symbol.
        If there's a change in the type create a Token instance.
        Yield a Token.

        Raises:
        TypeError -- when s is not a string object
        """
        self.s = s
        if not isinstance(s, str):
            raise TypeError("You can only tokenize string objects!")
        f = 0  # variable for the start position of a token
        for i, x in enumerate(s):
            # start with the second symbol
            if not i == 0:
                # save the type of the previous symbol
                prevt = self.check_typ(s[i-1])
                # check for the change of type
                if prevt != self.check_typ(x):
                    l = i - 1   # set the last position for the token
                    tok = Token(s[f:l+1], f, l, prevt)
                    yield tok
                    f = i
                    continue
                continue
        # create the token at the end of the string
        if not len(s) == 0:
            l = len(s)-1
            tok = Token(s[f:l+1], f, l, self.check_typ(s[len(s)-1]))
            yield tok
            

    def tokenize(self, s):
        """
        Take a string and return a list of Tokens.

        Check the type of the current and previous symbol.
        If there's a change in the type create a Token instance.
        Add Token to the list.
        At the end of the string create the last Token. 
        """
        self.s = s
        if not isinstance(s, str):
            raise TypeError("You can only tokenize string objects!")
        f = 0  # variable for the start position of a token
        tl = []
        for i, x in enumerate(s):
            # start with the second symbol
            if not i == 0:
                # save the type of the previous symbol
                prevt = self.check_typ(s[i-1])
                # check for the change of type
                if prevt != self.check_typ(x):
                    l = i - 1   # set the last position for the token
                    tok = Token(s[f:l+1], f, l, prevt)
                    tl.append(tok)
                    f = i
                    continue
                continue
        # create the token at the end of the string
        if not len(s) == 0:
            l = len(s)-1
            tok = Token(s[f:l+1], f, l, self.check_typ(s[len(s)-1]))
            tl.append(tok)
        return(tl)

if __name__ == '__main__':
    t = Tokenizer()
    for i in t.alph_tokenize('b'):
        print(i)
