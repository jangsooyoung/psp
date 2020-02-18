# -*- coding: utf-8 -*-
from io import BytesIO
import sys, os
import PspConfig

class Gen:

    begin_source = 1
    begin_var = 2
    end_mark = 3
    block_begin = 4
    block_end = 5
    line=0
    tabsz=PspConfig.tab
    space="                                                                                           "
    def fileToString(self, p_file):
        with open(p_file, 'r') as file:
            return file.read()

    def seeToken(self, c):
        if self.source_len <= c + 1:
            return 0, None
        if c + 3 <= self.source_len and self.source[c:c+3] == '<%=':
            return 3, self.begin_var
        if c + 5 <= self.source_len and self.source[c:c+5] == '<%{%>':
            return 5, self.block_begin
        if c + 6 <= self.source_len and self.source[c:c+5] == '<%}%>':
            print('self.block_end')
            return 6, self.block_end
        if c + 2 <= self.source_len and self.source[c:c+2] == '<%':
            return 2, self.begin_source
        return 1, self.source[c]

    def findHtmlEnd(self, c):
        while c < self.source_len and self.source[c] != "\n":
            if c + 2 <= self.source_len and \
                self.source[c + 0] == '<' and \
                self.source[c + 1] == '%':
                return c, False
            c += 1
        return c, True
    def findKeyword2(self, c, key):
        while c + 1 < self.source_len and (self.source[c] != key[0] or self.source[c+1] != key[1]):
            c += 1
        return c

    def parse(self, psp_name, py_name):
        self.source = self.fileToString(psp_name)
        self.source_len = len(self.source)

        with open(py_name, 'w') as gen:
            #self.source = list(text)
            c = 0
            gen.write("# -*- coding: utf-8 -*-\n")
            gen.write("from io import BytesIO\n")
            gen.write("import sys, os\n")
            gen.write("from pspconfig import PspConfig\n")
            gen.write("def call_psp_(http_handler, args):\n")
            gen.write("    _psp_out_ = BytesIO()\n")
            while True:
                sz, tok = self.seeToken(c)
                if sz == 0:
                    break;
                elif tok == self.block_begin:
                    c += sz
                    self.tabsz += 4
                elif tok == self.block_end:
                    c += sz
                    self.tabsz -= 4
                elif tok == self.begin_source:
                    c += sz
                    n = self.findKeyword2(c, "%>")
                    gen.write(self.tab()+''.join(self.source[c:n]).replace('\n', '\n'+self.tab()))
                    c = (n + 2)
                    gen.write('\n')
                elif tok == self.begin_var:
                    c += sz
                    n = self.findKeyword2(c, "%>")
                    gen.write(self.tab()+"_psp_out_.write(" + ''.join(self.source[c:n]) + ".encode())\n")
                    c = (n + 2)
                else:
                    # <%, line feed 나올떄 까지  읽기
                    n, is_line_end = self.findHtmlEnd(c)
                    stmt = ''.join(self.source[c: n]).replace('\"', '\\\"')
                    if is_line_end:
                        gen.write(self.tab()+"_psp_out_.write(\"" + stmt + "\\n\".encode())\n")
                        c = n + 1
                    else :
                        gen.write(self.tab()+"_psp_out_.write(\"" + stmt + "\".encode())\n")
                        c = n
            gen.write(self.tab()+"return _psp_out_\n")
        print("generate {}".format(py_name))
    def tab(self):
        return self.space[0:self.tabsz]

if __name__ == '__main__':
    p = Gen()
    if len(sys.argv) <= 1:
        print('usage: psp to pytheon code_generator')
        print('        python -g psp.py file[.psp]')
        print('            file.psp ==> file.py ')
        print('            ex) html_code<% python code %>  html_code <%=var%> html_code ')

    for f in sys.argv[1:]:
        psp_name = f.replace(".psp", "") + ".psp"
        py_name  = f.replace(".psp", "") + ".py"
        if os.path.isfile(psp_name):
            p.parse(psp_name, py_name)

