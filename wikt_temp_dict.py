"""Module that creates a stem database of russian nouns."""
import mwclient
import re
import shelve
import threading
from threading import Thread
import datetime
import os

templates = set()
stem_dict = {}

def download_templates(words):
    for line in words:
        #print(line)
        page = mwclient.page.Page(site, line)
        delim = '=== Морфологические и синтаксические свойства ==='
        # find part of the page that contains info about morphology
        try:
            t = page.text().split(delim)[1]
        except IndexError:
            continue
        t = t.split('===')[0].split('|')
        #print(t)
        try:
            temp_name = t[0].split('{{')[1] # find name of the template
        except IndexError:
            continue
        #if len(temp_name.split()) < 5:
            #print(temp_name)
         #   continue
        if ("сущ" not in temp_name) or ("ru" not in temp_name):
            if "Фам" not in temp_name:
                continue
        temp_name = "Шаблон:{0}".format(temp_name).strip()
        #print(temp_name)
        for l in t:
            if "основа" in l:
                l = l.split("=")
                try:
                    stem = l[1].strip() # stem of the word
                except IndexError:
                    continue
                if stem == "":
                    continue
                stem = stem.replace("́", "")
                stem = stem.replace("̀", "")
                var = l[0] # variable containing the stem
                templates.add(temp_name)
                if not stem == "":
                    stem_dict.setdefault(stem, {}).setdefault((temp_name, var), line)
    proc = threading.get_ident() # thread id
    print('Thread id {0} wrote down {1} words'.format(proc, len(words)))
    print('Dictionary has {0} entries'.format(len(stem_dict)))

if __name__ == "__main__":
    site = mwclient.Site("ru.wiktionary.org")
    nouns_set = sorted(list(line.strip() for line in open("final_nouns.txt", 'r', encoding='utf-8')))
    print(len(nouns_set))
    size = len(nouns_set)//15
    div_set = lambda st, sz: [st[i:i+sz] for i in range(0, len(st), sz)]
    # divide the set into subset of equal length
    lists = div_set(nouns_set, size)
    procs = [] # threads
    start_time = datetime.datetime.now()
    # create thread for each subset
    for index, word_list in enumerate(lists):
        print(index, len(word_list))
        proc = Thread(target=download_templates, args=(word_list,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print("Dictionary contains {0} stems".format(len(stem_dict)))
    db = shelve.open("stem.db", 'c')
    db.update(stem_dict)
    db.close()

    with open("templates.txt", 'w', encoding='utf-8') as f:
        for t in templates:
            s = t + "\n"
            f.write(s)
    
    print('Time elapsed: {}'.format(datetime.datetime.now() - start_time))
