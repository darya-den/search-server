import unittest
import shelve
import os
from morphan import Stemmer_simple, Stemmer_list, Stemmer_wiki, Stemmer_agent, Lemmatizer

class MyTestCase(unittest.TestCase):
    def test_simple_stem(self):
        st = Stemmer_simple(3)
        res = list(st.stemm_simple("энергопульсация"))
        stems = ["энергопульсация", "энергопульсаци", "энергопульсац", "энергопульса"]
        self.assertEqual(res, stems)

    def test_not_str(self):
        st = Stemmer_simple(3)
        with self.assertRaises(TypeError):
            list(st.stemm_simple(["j"]))

    def test_short(self):
        st = Stemmer_simple(3)
        res = list(st.stemm_simple("сыр"))
        stems = ["сыр"]
        self.assertEqual(res, stems)

    def test_list(self):
        inf = ("а", "е", "и", "о", "ы", "ю","я", "ей", "ем", "ой", "ом")
        st = Stemmer_list(inf)
        res = list(st.stemm_list("энергопульсация"))
        stems = ["энергопульсаци"]
        self.assertEqual(res, stems)

    def test_wiki(self):
        stem_dict = {"энергетик": {("Шаблон:шаблон", "основа") : "энергетика"}}
        inflect_dict = {"а": {("Шаблон:шаблон", "основа")}}
        stem = shelve.open("stem_test")
        stem.update(stem_dict)
        stem.close()
        inflexion = shelve.open("inflexion_test")
        inflexion.update(inflect_dict)
        inflexion.close()
        st = Stemmer_wiki("stem_test", "inflexion_test")
        res = list(st.stemm_wiki("энергетика"))
        stems = ["энергетик"]
        self.assertEqual(res, stems)
        os.remove("stem_test.db")
        os.remove("inflexion_test.db")

    def test_wiki_no(self):
        stem_dict = {"энергетик" : {("Шаблон:шаблон", "основа") : "энергетика"}}
        inflect_dict = {"а": (("Шаблон:шаблон", "основа"))}
        stem = shelve.open("stem_test")
        stem.update(stem_dict)
        stem.close()
        inflexion = shelve.open("inflexion_test")
        inflexion.update(inflect_dict)
        inflexion.close()
        st = Stemmer_wiki("stem", "inflexion")
        res = list(st.stemm_wiki("энергопульсация"))
        stems = []
        self.assertEqual(res, stems)
        os.remove("stem_test.db")
        os.remove("inflexion_test.db")

    def test_stemmer_agent(self):
        st = Stemmer_agent()
        res = list(st.stem("энергопульсационный"))
        gold = ["энергопульсационны", "энергопульсационн"]
        self.assertEqual(res, gold)

    def test_lemmatizator(self):
        stem_dict = {"электричеств" : {("Шаблон:шаблон", "основа") : "электричество"}}
        inflect_dict = {"ом": {("Шаблон:шаблон", "основа")}}
        stem = shelve.open("stem_test")
        stem.update(stem_dict)
        stem.close()
        inflexion = shelve.open("inflexion_test")
        inflexion.update(inflect_dict)
        inflexion.close()
        lmtz = Lemmatizer("stem_test", "inflexion_test")
        res = list(lmtz.lemmatize("электричеством"))
        gold = ["электричество"]
        self.assertEqual(res, gold)
        os.remove("stem_test.db")
        os.remove("inflexion_test.db")
        

        
if __name__ == '__main__':
    unittest.main()
