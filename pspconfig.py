import sys, os

class PspConfig:
    def __init__(self):
        PspConfig.ip         = ''
        PspConfig.port       = 40077
        PspConfig.js_path    = PspConfig.fullpath('WEB')
        PspConfig.html_path  = PspConfig.fullpath('WEB')
        PspConfig.img_path   = PspConfig.fullpath('WEB')
        PspConfig.psp_path   = PspConfig.fullpath('WEB')
        PspConfig.py_path    = PspConfig.fullpath('WEB')
        PspConfig.gen_path   = PspConfig.fullpath('WEB')
        PspConfig.upload_path= PspConfig.fullpath('WEB/car')
        PspConfig.tab = 1
        PspConfig.session_timeout = 3
        sys.path.append(PspConfig.py_path)
        sys.path.append(PspConfig.gen_path)
    def fullpath(p):
        if not p.startswith("/"):
            return os.getcwd() + "/" + p
        return p 
       

