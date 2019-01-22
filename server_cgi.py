from http.server import HTTPServer, CGIHTTPRequestHandler
import cgi
import html
from search_eng import SearchEngine
from tokenizer_gen import Tokenizer
from f_indexator import Position_d

class myRequestHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        resp_str = ""
        resp_str += "<html><body>"
        resp_str += "<form method=\"POST\" action=\"\">"
        resp_str += "<p> Введите поисковой запрос: "
        resp_str += "<input type=\"text\" name=\"QUERY\"><input type=\"submit\"></p>"
        resp_str += "<p> Сколько выдать документов: "
        resp_str += "<input type=\"text\" name=\"LIMIT\"></p>"
        resp_str += "<p> Начиная с какого: "
        resp_str += "<input type=\"text\" name=\"OFFSET\"></p>"
        resp_str += "<p> Сколько выдать цитат: "
        resp_str += "<input type=\"text\" name=\"LIM\"></p>"
        resp_str += "<p> Начиная с какой: "
        resp_str += "<input type=\"text\" name=\"OFF\"></p>"
        resp_str += "</form></body></html>"
        self.wfile.write(bytes(resp_str, 'utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE': 'text/html; charset=utf-8',
                    })
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        query = form.getfirst("QUERY", "")
        query = html.escape(query)
        limit = form.getfirst("LIMIT", "2") # document limit
        limit = int(html.escape(limit))
        offset = form.getfirst("OFFSET", "1") # document offset
        offset = int(html.escape(offset))
        mass0 = form.getfirst("OFF", "1") # initial cit offset
        mass0 = int(html.escape(mass0))
        mass1 = form.getfirst("LIM", "10") # initial citat limit
        mass1 = int(html.escape(mass1))
        cit_lim = form.getlist("NEW_LIM")
        cit_off = form.getlist("NEW_OFF")
        button_prev = form.getlist("PREV_PAGE")
        button_next = form.getlist("NEXT_PAGE")
        doc_prev = form.getlist("PREV_DOCS")
        doc_next = form.getlist("NEXT_DOCS")
        reset = form.getlist("RESET")
        print(doc_prev, doc_next)
        mass = []
        if not button_prev:
            if not button_next:
                if not cit_lim:
                    for i in range(limit):
                        mass.append((mass0 - 1, mass1 + 1)) # default array of (offset, limit) pairs
                else:
                    for i in range(limit):
                        mass.append((int(cit_off[i]) - 1, int(cit_lim[i]) + 1))
            else:
                for i in range(limit):
                    #print(i, button_next[0])
                    if not i == int(button_next[0]):
                        mass.append((int(cit_off[i]) - 1, int(cit_lim[i]) + 1))
                    else:
                        #print(mass0, mass1)
                        mass.append((int(cit_off[i]) - 1 + int(cit_lim[i]), int(cit_lim[i]) + 1))
        else:
            for i in range(limit):
                if not i == int(button_prev[0]):
                    mass.append((int(cit_off[i]) - 1, int(cit_lim[i]) + 1))
                else:
                    mass.append((int(cit_off[i]) - 1 - int(cit_lim[i]), int(cit_lim[i]) + 1))
        mass.append((0,0))
        print(mass)
        if doc_prev:
            offset = offset - limit
        if doc_next:
            offset = offset + limit
        #print(query)
        se = self.server.se
        width = int(self.server.config["Default"]["context w width"])
        t = Tokenizer().alph_tokenize(query)
        if len(list(t)) > 1:
            r = se.search_mult(query, limit + 1, offset - 1)
        else:
            r = se.search(query, limit + 1, offset - 1)
        cws = se.get_context_w(r, width)
        comb = se.combine_cw(cws)
        res = se.ultimate_out(comb, mass)
        print(res)
        if reset:
            out = ""
            out += "<html><body>"
            out += "<form method=\"POST\" action=\"\">"
            out += "<p> Введите поисковой запрос: "
            out += "<input type=\"text\" name=\"QUERY\"><input type=\"submit\"></p>"
            out += "<p> Сколько выдать документов: "
            out += "<input type=\"text\" name=\"LIMIT\"></p>"
            out += "<p> Начиная с какого: "
            out += "<input type=\"text\" name=\"OFFSET\"></p>"
            out += "<p> Сколько выдать цитат: "
            out += "<input type=\"text\" name=\"LIM\"></p>"
            out += "<p> Начиная с какой: "
            out += "<input type=\"text\" name=\"OFF\"></p>"
            out += "</form></body></html>"
        else:
            out = ""
            out += "<!DOCTYPE HTML><html><body>"
            out += "<form method=\"POST\" action=\"\">"
            out += "<p> Введите поисковой запрос: "
            out += "<input type=\"text\" name=\"QUERY\" value=\"{}\"><input type=\"submit\"></p>".format(query)
            out += "<p> Сколько выдать документов: "
            out += "<input type=\"text\" name=\"LIMIT\" value=\"{}\"></p>".format(limit)
            #out += "<p> Начиная с какого: "
            out += "<p><input type=\"text\" name=\"OFFSET\" hidden=\"true\" value=\"{}\"></p>".format(offset)
            #out += "<p> Сколько выдавать цитат: "
            out += "<input type=\"hidden\" name=\"LIM\" hidden=\"true\" value=\"{}\"></p>".format(mass1)
            #out += "<p> Начиная с какой: "
            #out += "<input type=\"text\" name=\"OFF\" hidden=\"true\" value=\"{}\"></p>".format(mass0)
            if not offset == 1:
                out += "<p><button type=\"submit\" name=\"PREV_DOCS\" value=\"prev\">Предыдущие документы</button>"
            if not len(res) < limit + 1:
                filenames = sorted(res.keys())[:-1]
                print(filenames)
                out += "<button type=\"submit\" name=\"NEXT_DOCS\" value=\"next\">Следующие документы</button></p>"
            else:
                filenames = sorted(res.keys())
            out += "<ol>"
            for ind, r in enumerate(filenames):
                quotes = list(res[r])
                out += "<li><p><b>{}</b></p><ul>".format(r)
                for qi, q in enumerate(quotes):
                    if not qi == mass[ind][1] - 1:
                        out += "<li>{}</li>".format(q)
                out += "</ul></li>"
                out += "<p> Сколько цитат показать? "
                out += "<input type=\"text\" name=\"NEW_LIM\" value=\"{}\"></p>".format(mass[ind][1] - 1)
                print(mass[ind])
                if not mass[ind][0] == 0:
                    out += "<p><button type=\"submit\" name =\"PREV_PAGE\" value=\"{}\">Предыдущая страница</button>".format(ind)
                print(len(quotes))
                if not len(quotes) < mass[ind][1]:
                    out += "<button type=\"submit\" name=\"NEXT_PAGE\" value=\"{}\">Следующая страница</button></p>".format(ind)
                #out += "<p> Начиная с какой? "
                out += "<input type=\"text\" name=\"NEW_OFF\" hidden=\"true\" value=\"{}\"></p>".format(mass[ind][0] + 1)
            out += "</ol>"
            out += "<p><button type=\"submit\" name=\"RESET\" value=\"reset\">Назад к странице поиска</button></p></body></html>"
        self.wfile.write(bytes(out, 'utf-8'))
        
def run(server_class=HTTPServer, handler_class=myRequestHandler):
    server_adress = ('127.0.0.1', 8081)
    httpd = server_class(server_adress, handler_class)
    httpd.config = configparser.ConfigParser()
    httpd.config.read("config.ini")
    db = httpd.config["Default"]["db"]
    #db = "wap_stem" # your database
    httpd.se = SearchEngine(db)
    try:
        httpd.serve_forever()
    except:
        del httpd.se

if __name__ == '__main__':
    run()
