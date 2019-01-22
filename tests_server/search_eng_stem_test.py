import unittest
import shelve
from f_indexator import Indexator, Position_d
import os
from search_engimport SearchEngine, ContextWindow

class MyTestCase(unittest.TestCase):
    def test_search_mult(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("электричество — совокупность явлений, обусловленных существованием, взаимодействием и движением электрических зарядов.")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("электрический заряд (количество электричества) — это физическая скалярная величина, определяющая способность тел быть источником электромагнитных полей и принимать участие в электромагнитном взаимодействии.")
        file2.close()
        ind.stem_indexate("test.db", file1.name)
        ind.stem_indexate("test.db", file2.name)   
        se = SearchEngine("test.db")
        res = se.search_mult_stem"электрическое взаимодействие", 2, 0)
        for r in res:
            res[r] = list(res[r])
        gold = {file1.name: [Position_d(68, 82, 0), Position_d(96, 108, 0)],
                file2.name: [Position_d(0, 12, 0), Position_d(191, 204, 0)]}
        self.assertEqual(res, gold)
        del se
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.db")
        #os.remove("test.db.bak")
        #os.remove("test.db.dat")
        #os.remove("test.db.dir")

    def test_search_oneword(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("электричество — совокупность явлений, обусловленных существованием, взаимодействием и движением электрических зарядов.")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("электрический заряд (количество электричества) — это физическая скалярная величина, определяющая способность тел быть источником электромагнитных полей и принимать участие в электромагнитном взаимодействии.")
        file2.close()
        ind.stem_indexate("test.db", file1.name)
        ind.stem_indexate("test.db", file2.name)   
        se = SearchEngine("test.db")
        res = se.search_stem("электрическое", 2, 0)
        for r in res:
            res[r] = list(res[r])
        gold = {file1.name: [Position_d(96, 108, 0)],
                file2.name: [Position_d(0, 12, 0)]}
        self.assertEqual(res, gold)
        del se
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.db")
        #os.remove("test.db.bak")
        #os.remove("test.db.dat")
        #os.remove("test.db.dir")

    def test_search(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("мама мыла раму\nмаме мыли раму")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("рама была помыта мамой\nрама была помыта для мамы")
        file2.close()
        ind.stem_indexate("test.db", file1.name)
        ind.stem_indexate("test.db", file2.name)   
        se = SearchEngine("test.db")
        res = se.search_stem("мама", 2, 0)
        for r in res:
            res[r] = list(res[r])
        gold = {file1.name: [Position_d(0, 3, 0), Position_d(0, 3, 1)],
                file2.name: [Position_d(17, 21, 0), Position_d(21, 24, 1)]}
        self.assertEqual(res, gold)
        del se
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.db")
        #os.remove("test.db.bak")
        #os.remove("test.db.dat")
        #os.remove("test.db.dir")
    
                

if __name__ == '__main__':
    unittest.main()
