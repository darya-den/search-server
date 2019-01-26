# search-server
Web server with search engine.
The search engine server works in two modes: with morhological analysis (for Russian nouns) and without.

The modules deal with various tasks:
— tokenization
— document indexing
— construction of context windows and citations
— server inteface
— stemming and lemmatization
## Simple server without morphological analysis

Server works with an indexed database containing the reqired documents. Each file is tokenized (divided into alphabetical sequences) and for each token information about its position in document is saved in the db.
To indexate the files use *db_file_indexate* method fron **f_indexator.py**:
```
from f_indexator import Indexator

ind = Indexator()
ind.db_file_indexate("my_db.db", "my_file.txt")
```
To run the server simply run the **server_cgi.py** file.

## Server with morphology

Here instead of the token we save stems or lemmas of the word to the database. For that we need additional morphological databases. 

### Creating morphological databases

One way to start building databases is to dowload the list of Russian nouns from [ru.wiktionary.org](https://ru.m.wiktionary.org/wiki/Заглавная_страница) with **wiktionary.py** module.
Alternatively, **final_nouns.txt** file can be used but Wiktionary is always changing and this file is relevant to November, 2018.

Then, we need stem database: run **wikt_temp_dict.py**; and inflexion database: run **wikt_inflexions.py**.

Now we have everything for our morphological analysis and we can indexate our documents (*stem_indexate* method from **f_indexator.py**):
```
from f_indexator import Indexator

ind = Indexator()
ind.stem_indexate("my_stem_db.db", "my_file")
```
To run the server with the morphology simply run **server_cgi_stem.py**

## Default parameters

Default values for different variables are in the **config.ini** file. 

## Tests

Tests for several modules are available in the *test_server* directory
