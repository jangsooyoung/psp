# -*- coding: utf-8 -*-
from io import BytesIO
import sys, os
from pspconfig import PspConfig
def call_psp_(http_handler, args):
    _psp_out_ = BytesIO()
    
    import os.path
    import glob
    from pspconfig import PspConfig 
    
    _psp_out_.write("\n".encode())
    import tensorflow as tf
    _psp_out_.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"><html>\n".encode())
    _psp_out_.write("<title>Upload Result Page</title>\n".encode())
    _psp_out_.write("<meta http-equiv=\"Pragma\" content=\"no-cache\">\n".encode())
    _psp_out_.write("<meta http-equiv=\"Expires\" content=\"0\">\n".encode())
    _psp_out_.write("<html> \n".encode())
    _psp_out_.write("<title> Car/ license plate recognition</title>\n".encode())
    _psp_out_.write("<body>\n".encode())
    _psp_out_.write("<script type=\"text/javascript\">\n".encode())
    _psp_out_.write("function del(fname) { \n".encode())
    _psp_out_.write("    yn = confirm(fname + '이미지를  삭제 하시겠습니까 ? ')\n".encode())
    _psp_out_.write("    if (yn == true) {\n".encode())
    _psp_out_.write("        location.href='/index.psp?del='+fname;\n".encode())
    _psp_out_.write("    } \n".encode())
    _psp_out_.write("}\n".encode())
    _psp_out_.write("</script>\n".encode())
    
    s = http_handler.getSession()
    if "cnt" not in s:
        s["cnt"] = 0
    s["cnt"] += 1
    
    display_image="car/default.jpg"
    if "del" in args:
        file_name=args["del"]
        print('del', PspConfig.img_path + file_name)
        if os.path.isfile(PspConfig.img_path + file_name):
            os.remove(PspConfig.img_path  + file_name)
            print('remove', PspConfig.img_path + file_name)
    elif "upfile" in args:
        filename = args['upfile'].filename
        if filename != '':
            data = args['upfile'].file.read()
            open(PspConfig.upload_path  + "/" + filename, "wb").write(data)
            display_image="car/" +filename
    elif "image" in args:
        display_image=args["image"]
    
    _psp_out_.write("\n".encode())
    _psp_out_.write("<hr>\n".encode())
    _psp_out_.write("<ul>\n".encode())
    _psp_out_.write("<form ENCTYPE=\"multipart/form-data\"  action='/index.psp' method=\"post\"  >\n".encode())
    _psp_out_.write("<table>\n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("		<td colspan=2><h1><a hef='www.hanee.com'>License Plate Recognition Test</a></h1></td>\n".encode())
    _psp_out_.write("		<td><a href='/help.html?ver=0.007996558325123804'>HELP</a></td>\n".encode())
    _psp_out_.write("	</tr>\n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("	    <td colspan=3>\n".encode())
    _psp_out_.write("		PSP (Python server page, python jsp ) demo page<br>\n".encode())
    _psp_out_.write("        <a  target=\"_blank\" href=\"http://github.com/jangsooyoung/psp\">github.com/jangsooyoung/psp</a>\n".encode())
    _psp_out_.write("        </td>\n".encode())
    _psp_out_.write("	</tr>\n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("		<td colspan=3>\n".encode())
    _psp_out_.write("			<a href='/index.psp?image=".encode())
    _psp_out_.write(display_image.encode())
    _psp_out_.write("'>\n".encode())
    _psp_out_.write("				<img src='".encode())
    _psp_out_.write(display_image.encode())
    _psp_out_.write("' width=600  /></a>\n".encode())
    _psp_out_.write("			<br>\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("	</tr> \n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("		<td colspan=2><font size=2>-High resolution cell phone cameras. (Plate part is recommended at least 300 pix)</font>\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("	</tr>\n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("		<td><h2><font size=6>Result : 40 조 7220</font>\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("		<td>\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("		<td>\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("	</tr>\n".encode())
    _psp_out_.write("	<tr>\n".encode())
    _psp_out_.write("		<td>\n".encode())
    _psp_out_.write("			<input type=\"file\" style=\"WIDTH:200pt;HEIGHT:20pt\"  value=\"File\" name=\"upfile\"/>[jpg file]\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("		<td>\n".encode())
    _psp_out_.write("			<input type=\"submit\" style=\"WIDTH:120pt;HEIGHT:20pt\"  value=\"upload\" name=\"upload\" />\n".encode())
    _psp_out_.write("		</td>\n".encode())
    _psp_out_.write("	</tr>\n".encode())
    _psp_out_.write("</table>\n".encode())
    _psp_out_.write("</form>\n".encode())
    _psp_out_.write("<hr>\n".encode())
    _psp_out_.write("<ul>\n".encode())
    
    file_list = os.listdir(PspConfig.img_path + "/car/")
    for fname in [file for file in file_list if file.endswith(".jpg")]:
        _psp_out_.write("\n".encode())
        _psp_out_.write("	<li><font size=1>\n".encode())
        _psp_out_.write("			<a href=\"/index.psp?image=/car/".encode())
        _psp_out_.write(fname.encode())
        _psp_out_.write("\">[".encode())
        _psp_out_.write(fname.encode())
        _psp_out_.write("]</a>\n".encode())
        _psp_out_.write("				&nbsp;&nbsp;\n".encode())
        _psp_out_.write("			<a href=\"javascript:del('/car/".encode())
        _psp_out_.write(f'{fname}'.encode())
        _psp_out_.write("')\">d</a>\n".encode())
        _psp_out_.write("		</font>\n".encode())
        _psp_out_.write("	</li>\n".encode())
    _psp_out_.write("</ul>\n".encode())
    _psp_out_.write("</hr>\n".encode())
    _psp_out_.write("</body>\n".encode())
    _psp_out_.write("</html>\n".encode())
    return _psp_out_
