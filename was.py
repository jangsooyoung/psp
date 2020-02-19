from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Lock, Thread
from pspconfig import PspConfig
from urllib.parse import urlparse, parse_qs
import glob, importlib, os, pathlib, sys, posixpath, traceback, urllib, cgi, random
from gen import Gen
import http.cookies
from http import cookies
import time
from threading import Timer


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass
class Was(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send(None)

    def do_DELETE(self):
        self.send(None)

    def do_GET(self):
        self.getSession()
        parse_info = urlparse(self.path)
        print('do_GET=', self.path)
        args = {}
        if parse_info.query.find("=") >= 0:
            args = dict(qc.split("=") for qc in parse_info.query.split("&"))
        self.do_process(parse_info.path, args)

    def do_POST(self):
        self.getSession()
        print('do_POST=', self.path)
        parse_info = urlparse(self.path)
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        args = {}
        if ctype == 'multipart/form-data':
            args = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                   environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], })
        self.do_process(parse_info.path, args)

    def send(self, f):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        if f is not None:
            self.send_header("Content-Length", str(f.tell()))
            f.seek(0)
            self.copyfile(f, self.wfile)
            f.close()
        self.end_headers()

    def do_process(self, path, args):
        try:
            p = path
            if (p.endswith(".jpg") or p.endswith(".gif") or p.endswith(".bmp") or p.endswith(".png")) and \
                os.path.isfile(PspConfig.img_path + p):
                self.send_File(PspConfig.img_path + p)
            elif (p.endswith(".html") or p.endswith(".htm")) and os.path.isfile(PspConfig.html_path+p):
                self.send_File(PspConfig.html_path + p)
            elif (p.endswith(".js") or p.endswith(".js")) and os.path.isfile(PspConfig.js_path+p):
                self.send_File(PspConfig.js_path + p)
            elif (p.endswith(".css") or p.endswith(".css")) and os.path.isfile(PspConfig.css_path+p):
                self.send_File(PspConfig.css_path + p)
            elif p.endswith(".py")  and os.path.isfile(PspConfig.py_path + p):
                self.execute_py(py_name)
            elif p.endswith(".psp") and os.path.isfile(PspConfig.psp_path + p):
                self.execute_psp(p, args)
            # directory index
            elif os.path.isdir(PspConfig.psp_path + p) and os.path.isfile(PspConfig.psp_path + p + "index.psp"):
                self.execute_psp(p + "index.psp", args)
            elif os.path.isdir(PspConfig.py_path + p) and os.path.isfile(PspConfig.py_path + p + "index.py"):
                self.execute_py(PspConfig.py_path + p + "index.py", args)
            elif os.path.isdir(PspConfig.html_path + p) and os.path.isfile(PspConfig.html_path + p + "index.html"):
                self.send_File(PspConfig.html_path + p + "index.html", args)
            else:
                self.send_error(404, f"No permission to list directory..{path}")
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            self.send_response(301)
            self.send_header("location", "/")
            self.end_headers()

    def execute_psp(self, pname, args):
        psp_file = PspConfig.psp_path + pname
        py_file = PspConfig.gen_path  + pname.replace(".psp", ".py")
        if not os.path.isfile(py_file) or os.path.getmtime(psp_file) > os.path.getmtime(py_file):
            Gen().parse(psp_file, py_file)
        self.execute_py(py_file, args)

    def execute_py(self, py_name, args):
        print(os.path.join(PspConfig.psp_path, py_name))
        py_files = glob.glob(os.path.join(PspConfig.psp_path, py_name))
        module_name = pathlib.Path(py_files[0]).stem
        module = importlib.import_module(module_name)
        importlib.reload(module)

        out = module.call_psp_(self, args)

        length = out.tell()
        out.seek(0)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(length))
        self.send_header('Set-Cookie', self.cooki)
        self.end_headers()
        self.copyfile(out, self.wfile)
        out.close()

    def send_File(self, full_file_path):
        try:
            f = open(full_file_path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        ctype = self.guess_Type(full_file_path)

        self.send_response(200)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        if full_file_path.endswith('.html') or full_file_path.endswith('.htm'):
            self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        self.copyfile(f, self.wfile)
        f.close()

    def guess_Type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    def getSession(self):
        self.cooki = self.headers.get('Cookie')
        if self.cooki == None:
            self.cooki = f"S{random.random()}"
        session_id = self.cooki
        if session_id not in Was.session_list:
           Was.session_list[session_id] = {}
        s = Was.session_list[session_id]
        s['last_access']= time.time();
        return s

    def session_manager():
        #print('session_list', len(Was.session_list))
        base_time = time.time()
        for skey in list(Was.session_list.keys()):
            s = Was.session_list[skey]
            if s['last_access'] + PspConfig.session_timeout * 60 < base_time  :
                del Was.session_list[skey]
        Timer(60, Was.session_manager, ()).start()

if __name__ == '__main__':
    Was.session_list = {}
    cfg = PspConfig()
    server = ThreadingServer(('', cfg.port), Was)
    Timer(1, Was.session_manager, ()).start()
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print('Finished.')
