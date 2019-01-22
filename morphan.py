'''Module containing morphological analyses methods'''
import shelve
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Stemmer_agent(object):
    """Stemmer.

    methods: stem -- get the stem of the word.
                     As a default use Lemmatizator.
                     For Lemmatizator use Stemmer_wiki as fallback.
                     For Stemmer_wiki use Stemmer_list as fallback.
                     For Stemmer_list use Stemmer_simple as fallback."""
    def __init__(self):
        # Stemmer_simple
        mlength = int(config["Default"]["simple stemmer"])
        self.stem_simple = Stemmer_simple(mlength)
        # Stemmer_list
        infl_file = config["Default"]["inflexion file"]
        with open(infl_file, 'r', encoding='utf-8') as inf:
            endings = set(line.strip() for line in inf)
        self.stem_list = Stemmer_list(endings)
        # Stemmer_wiki
        stem_db = config["Default"]["stem sb"]
        inflex_db = config["Default"]["inflexion db"]
        self.stem_wiki = Stemmer_wiki(stem_db, inflex_db)
        # Lemmatizator
        self.lemmtzr = Lemmatizer(stem_db, inflex_db)

    def __del__(self):
        del self.stem_simple
        del self.stem_list
        del self.stem_wiki
        del self.lemmtzr
  
    def stem(self, s):
        """Get the stem of the word.

        First try to get the lemma with Lemmatizator.
        If it yield no lemma (i.e. no lemma can be found in db), use Stemmer_wiki.
        If Stemmer_wiki yields no stem (i.e. no stems and inflexions can be found in dbs),
        use Stemmer_list.
        If Stemmer_list yields no stem (i.e. word doesn't contain any endings from
        the list of endings), use Stemmer_simple"""
        res = list(self.lemmtzr.lemmatize(s))
        if not res:
            res = list(self.stem_wiki.stemm_wiki(s))
            if not res:
                res = list(self.stem_list.stemm_list(s))
                if not res:
                    res = list(self.stem_simple.stemm_simple(s))
        for r in res:
            yield r
            
class Lemmatizer(object):
    def __init__(self, stem_db, inflexion_db):
        """Initiate Lemmatizator with morphological databases.

        param: stem_db -- database with stems from ru.wiktionary.org
               Entries are: {stem: {(template, variable): lemma}}
               inflex_db -- database with inflexions from ru.wiktionary.org
               Entries are: {inflexion: ((template, variable))}"""
        self.stems = shelve.open(stem_db)
        self.inflexions = shelve.open(inflexion_db)

    def __del__(self):
        self.stems.close()
        self.inflexions.close()

    def lemmatize(self, s):
        """Get the lemma of the word.

        Divide the word into stem and the ending
        (starting with the ending as the last symbol of the word
        and and going on).
        For each such division check if the stem is in the stem database
        and the ending is in the inflexion database.
        If not, check the next division.
        If yes, check if the stem and the inflexion have the same template
        and variable name in the database.
        If there is a match -- yield the lemma from the database."""
        if not isinstance(s, str):
            raise TypeError("You can only stem str objects!")
        for i in range(1, len(s)-2):
            st = s[:-i]
            inf = s[-i:]
            # check that stem in in the stem database
            # or that inflexion is in the inflexions database
            # if not -- continue
            if st not in self.stems or inf not in self.inflexions:
                continue
            # find intersection of the stem and inflexion
            # i.e. commom template and variable name
            stem_tpl = set(self.stems[st].keys())
            com_tpl = stem_tpl.intersection(self.inflexions[inf])
            # if there is an intersection
            # yield lemma, associated with that template and variable
            if com_tpl:
                for tpl in com_tpl:
                    yield self.stems[st][tpl]

class Stemmer_wiki(object):
    """Stemming using the data from wiktionary."""
    def __init__(self, stem_db, inflex_db):
        """Initiate stemmer with morphological databases.

        param: stem_db -- database with stems from ru.wiktionary.org
               Entries are: {stem: {(template, variable): lemma}}
               inflex_db -- database with inflexions from ru.wiktionary.org
               Entries are: {inflexion: ((template, variable))}"""
        self.stems = shelve.open(stem_db)
        self.inflexions = shelve.open(inflex_db)

    def __del__(self):
        self.stems.close()
        self.inflexions.close()
        
    def stemm_wiki(self, s):
        """Get the stem of the word (based on the data from morphological
        databases).

        Divide the word into stem and the ending
        (starting with the ending as the last symbol of the word
        and and going on).
        For each such division check if the stem is in the stem database
        and the ending is in the inflexion database.
        If not, check the next division.
        If yes, check if the stem and the inflexion have the same template
        and variable name in the database.
        If there is a match -- yield the stem."""
        if not isinstance(s, str):
            raise TypeError("You can only stem str objects!")
        for i in range(1, len(s)-2):
            st = s[:-i]
            inf = s[-i:]
            # check that stem in in the stem database
            # or that inflexion is in the inflexions database
            # if not -- continue
            if st not in self.stems or inf not in self.inflexions:
                continue
            # find intersection of the stem and inflexion
            # i.e. commom template and variable name
            # if there is one -- yield the stem
            stem_temp = set(self.stems[st].keys())
            if stem_temp.intersection(self.inflexions[inf]):
                yield st
            
class Stemmer_list(object):
    """Stemming with the set of endings"""
    def __init__(self, endings):
        self.endings = endings
        
    def stemm_list(self, s):
        """Get the stem of the word (based on the set of endings).

        For strings longer that 3 symbols see if the last symbols
        are in the set of endings (how many symbols to look at is determined by min and max length
        of endings in self.endings).
        If yes, delete the ending and yield the stem; if no, continue.
        return: strings
        param: s -- string
        """
        if not isinstance(s, str):
            raise TypeError("You can only stem str objects!")
        m = max(len(x) for x in self.endings) # max length of inflection
        n = min(len(x) for x in self.endings) # min length of inflection
        if len(s) > m:
            for i in range(n, m+1):
                if not i:
                    yield s
                else:
                    if s[-i:] in self.endings: # check in ending i
                        yield s[:-i]
        else:
            yield s

class Stemmer_simple(object):
    """Stemming with max length of the ending."""
    def __init__(self, mlength):
        self.mlength = mlength
        
    def stemm_simple(self, s):
        """Get the stem of the word (based on the max length of the ending).

        For strings longer that mlength symbols, delete the last 0-mlength symbols
        and yield the stem.
        return: strings
        param: s -- string"""
        if not isinstance(s, str):
            raise TypeError("You can only stem str objects!")
        yield s
        if len(s) > self.mlength:
            for i in range(1, self.mlength+1):
                yield s[:-i]


if __name__ == "__main__":
    st = Stemmer_agent()
    for s in st.stem("электричеством"):
        print(s)
    lmtzr = Lemmatizator()
    for l in lmtzr.lemmatize("электричеством"):
        print(l)
