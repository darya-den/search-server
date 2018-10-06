"""Unittest for f_indexator module"""

import unittest
import os
import shelve
from f_indexator import Indexator, Position_ext, Position_d


class MyTestCase(unittest.TestCase):
    def test_index(self):
        ind = Indexator()
        file = open("testing.txt", 'w', encoding="utf-8")
        file.write("1) тестируем \n2) тестируем!")
        file.close()
        dic = ind.file_indexate(file.name)
        refrd = {"1":[Position_ext(0, 0, file.name, 0)],
                 "тестируем": [Position_ext(3, 11, file.name, 0),
                               Position_ext(3, 11, file.name, 1)],
                 "2":[Position_ext(0, 0, file.name, 1)]}
        self.assertEqual(dic, refrd)
        os.remove('testing.txt')


    def test_index_d(self):
        ind = Indexator()
        file = open("testing.txt", 'w', encoding="utf-8")
        file.write("1) тестируем \n2) тестируем!")
        file.close()
        dic = ind.lfile_indexate(file.name)
        refrd = {"1": {file.name:[Position_d(0, 0, 0)]},
                 "тестируем": {file.name : [Position_d(3, 11, 0),
                               Position_d(3, 11, 1)]},
                 "2": {file.name: [Position_d(0, 0, 1)]}}
        self.assertEqual(dic, refrd)
        os.remove('testing.txt')

    def test_dbind(self):
        ind = Indexator()
        file1 = open("f1.txt", 'w', encoding="utf-8")
        file1.write("123 hello!")
        file1.close()
        file2 = open("f2.txt", 'w', encoding="utf-8")
        file2.write("well\n 123--")
        file2.close()
        ind.db_file_indexate("test.db", file1.name)
        ind.db_file_indexate("test.db", file2.name)
        refrd = {"123":{file1.name: [Position_d(0, 2, 0)],
                        file2.name: [Position_d(1, 3, 1)]},
                 "hello":{file1.name: [Position_d(4, 8, 0)]},
                 "well":{file2.name: [Position_d(0, 3, 0)]}}
        with shelve.open("test.db") as dic:
            self.assertEqual(dict(dic), refrd)
        os.remove("f1.txt")
        os.remove("f2.txt")
        os.remove("test.db.bak")
        os.remove("test.db.dat")
        os.remove("test.db.dir")
        

if __name__ == '__main__':
    unittest.main()
