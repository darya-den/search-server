import unittest
from f_indexator import Indexator, Position_d
import os
from search_eng import SearchEngine, ContextWindow


class MyTestCase(unittest.TestCase):
    def test_search(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello!")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("well\n 123--")
        file2.close()
        ind.db_file_indexate("test.db", file1.name)
        ind.db_file_indexate("test.db", file2.name)
        se = SearchEngine("test.db")
        res = se.search("123")
        refrd = {file1.name: [Position_d(0, 2, 0)],
                 file2.name: [Position_d(1, 3, 1)]}
        self.assertEqual(res, refrd)
        del se
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.bak")
        os.remove("test.db.dat")
        os.remove("test.db.dir")

    def test_s_mult(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello!")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("well\n 123--")
        file2.close()
        ind.db_file_indexate("test.db", file1.name)
        ind.db_file_indexate("test.db", file2.name)
        se = SearchEngine("test.db")
        res = se.search_mult("123 hello")
        refrd = {file1.name: [Position_d(0, 2, 0), Position_d(4, 8, 0)]} 
        self.assertEqual(res, refrd)
        del se
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.bak")
        os.remove("test.db.dat")
        os.remove("test.db.dir")

    def test_context(self):
        self.skipTest("")
        se = SearchEngine()
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello! how are you doing, tell me! \ni am doing just fine, hello! 123")
        file1.close()
        res = se.get_context_w({file1.name: [Position_d(23, 27, 0), Position_d(5, 9, 1)]}, 2)
        #print(res)
        refrd = {file1.name : [ContextWindow([Position_d(23, 27, 0)], "123 hello! how are you doing, tell me! \n", 2),
                               ContextWindow([Position_d(5, 9, 1)], "i am doing just fine, hello! 123", 2)]}
        #cw = ContextWindow(Position_d(23, 27, 0), "123 hello! how are you doing, tell me! \n", 2)
        #print(cw.line, cw.left, cw.right)
        self.assertEqual(res, refrd)
        os.remove("f1.txt")

    def test_get_word(self):
        self.skipTest("")
        se = SearchEngine()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello!")
        file1.close()
        res = se.get_word("f1.txt", Position_d(4, 8, 0))
        refr = "hello" 
        self.assertEqual(res, refr)
        os.remove("f1.txt")

    def test_combinecws(self):
        self.skipTest("")
        se = SearchEngine()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello! Well how are you doing, tell me right now! \ni am doing just fine, hello! 123")
        file1.close()
        cws = se.get_context_w({file1.name: [Position_d(24, 26, 0), Position_d(28, 32, 0)]}, 2)
        #print(cws)
        res = se.combine_cw(cws)
        #print(res)
        refrd = {file1.name : [ContextWindow([Position_d(24, 26, 0), Position_d(28, 32, 0)],
                                             "123 hello! Well how are you doing, tell me right now! \n", 2)]}
        self.assertEqual(res, refrd)
        os.remove("f1.txt")


    def test_ult(self):
        self.skipTest("")
        se = SearchEngine("")
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello! Well how are you doing, tell me right now!")
        file1.close()
        res = se.ultimate_out({file1.name : [ContextWindow([Position_d(24, 26, 0), Position_d(28, 32, 0)],
                                             "123 hello! Well how are you doing, tell me right now!", 2)]})
        #print(res)
        refrd = {file1.name : ["Well how are <b>you</b> <b>doing</b>, tell me right now!"]}
        self.assertEqual(res, refrd)
        os.remove("f1.txt")


    def test_compl(self):
        self.skipTest("")
        se = SearchEngine()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("Нужно проверить, работает ли контекстное окно \n для разных контекстов!")
        file1.close()
        res = se.ultimate_out({file1.name:[ContextWindow([Position_d(17, 24, 0), Position_d(26, 27, 0)],
                                                         "Нужно проверить, работает ли контекстное окно \n", 1),
                                           ContextWindow([Position_d(5, 10, 1)], " для разных контекстов!", 1)]})
        print(res)
        refrd = {file1.name: ["Нужно проверить, <b>работает</b> <b>ли</b> контекстное окно \n",
                              "для <b>разных</b> контекстов"]}
        self.assertEqual(res, refrd)
        os.remove("f1.txt")


if __name__ == '__main__':
    unittest.main()
