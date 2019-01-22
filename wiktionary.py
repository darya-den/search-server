"""Module that dowloads all Russian nouns from ru.wiktionaty.org using multiple Threads"""

import os
import mwclient
import datetime
from threading import Thread

site = mwclient.Site("ru.wiktionary.org")
namespace = 14 # 14 is the namespace of a category
cat = site.pages['Category:Русские существительные'] # the root
visited_nodes = set() # set of visited categories and pages
restricted = ["Категория:Существительные в винительном падеже/ru",
              "Категория:Существительные в дательном падеже/ru",
              "Категория:Существительные в звательном падеже/ru",
              "Категория:Существительные в предложном падеже/ru",
              "Категория:Существительные в разделительном падеже/ru",
              "Категория:Существительные в родительном падеже/ru",
              "Категория:Существительные в творительном падеже/ru"]
for r in restricted:
    visited_nodes.add(r)

def download_nodes(filename, page):
    cat_list = []
    with open(filename, 'w', encoding='utf-8') as f:
        cat_list.append(page)
        for page in cat_list:
            print(page.name)
            if page.name not in visited_nodes: # check if it has already been visited
                visited_nodes.add(page.name)
                for article in page: # look through pages and subcategories in category
                    if article.name in visited_nodes:
                        continue
                    # if it hasn't been visited
                    if article.namespace == namespace: # check if its category
                        cat_list.append(article) # add to list of categories so that we can visit it later
                    else:
                        # add the name of the page to the visited list
                        # and then write it into the file
                        visited_nodes.add(article.name)
                        string = article.name + "\n"
                        f.write(string)
                proc = threading.get_ident() # thread id
                print('Thread id {0} wrote down pages of {1} in {2}'.format(proc, page.name, filename))
        

if __name__ == '__main__':
    procs = [] # list of Threads
    start_time = datetime.datetime.now()
    page_list = [] # list for the subcategories of the root
    file1 = "rn.txt"
    files = [] # list of filenames (one for each Thread)
    files.append(file1)
    # download the root (Category:Русские существительные)
    with open(file1, 'w', encoding='utf-8') as f:
        print(cat.name)
        for article in cat:
            if article.namespace == namespace:
                page_list.append(article)
            else:
                visited_nodes.add(article.name)
                string = article.name + "\n"
                f.write(string)
    # create a Thread for each subcategory of the root
    for index, page in enumerate(page_list):
        # file for the Thread
        # because multiple Threads can't write to the same file
        filename = "{0}.txt".format(index) 
        files.append(filename)
        # define Thread and its function
        proc = Thread(target=download_nodes, args=(filename, page,))
        procs.append(proc)
        proc.start() # start the Thread

    # join the Threads
    # i.e. wait for all of them to finish before executing the next piece of code
    for proc in procs:
        proc.join()
        
    # write nouns from all the Thread files into one single file
    with open("final_nouns.txt", 'w', encoding='utf-8') as outfile:
        for file in files:
            with open(file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line)
            os.remove(file)
            
    print('Time elapsed: {}'.format(datetime.datetime.now() - start_time))
