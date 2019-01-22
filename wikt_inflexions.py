import mwclient
import re
import shelve
import threading
from threading import Thread
import datetime
import os

inflex_dict = {}

def download_inflex(templates):
    for line in templates:
        page = mwclient.page.Page(site, line)
        for l in page.text().split("|"):
            # find parts of the page that contain info about inflexions
            if "основа" in l:
                try:
                    l = l.split("{{{")[1]
                except IndexError:
                    continue
                # find what variable the inflexion combines with
                l = re.split("}+", l)
                var = l[0]
                try:
                    # find the inflexion
                    inflex = l[1].strip()
                    inflex = inflex.replace("́", "")
                    inflex = inflex.replace("̀", "")
                    # get rid of any non-alphabetic symbols
                    inflex = re.split("\W+", inflex)[0]
                except IndexError:
                    continue
                # check if the inflexion is not a zero one
                if not inflex == "":
                    inflex_dict.setdefault(inflex, set()).add((line, var))
    proc = threading.get_ident() # thread id
    print('Thread id {0} wrote down {1} templates'.format(proc, len(templates)))
    print('Dictionary of inflexions has {0} entries'.format(len(inflex_dict)))


if __name__ == "__main__":
    site = mwclient.Site("ru.wiktionary.org")
    # file with templates
    temp_set = sorted(list(line.strip() for line in open("templates.txt", 'r', encoding='utf-8')))
    size = len(temp_set)//10
    # divide the file into (sort of) equal parts
    lists = [temp_set[i:i+size] for i in range(0, len(temp_set), size)]
    procs = [] # threads
    start_time = datetime.datetime.now()
    # create thread for each subset
    for index, word_list in enumerate(lists):
        print(index, len(word_list))
        proc = Thread(target=download_inflex, args=(word_list,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print("Dictionary contains {0} stems".format(len(inflex_dict)))
    db = shelve.open("inflexion", 'c')
    db.update(inflex_dict)
    db.close()

    print('Time elapsed: {}'.format(datetime.datetime.now() - start_time))
