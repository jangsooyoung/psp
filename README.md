psp : python jsp, python server page 
	jsp functionality in python that works in a similar way to jsp
	WEB/WAS Service 

	Sample PSP Code
		Html code 
		<% python code %>
		<%= python variable %>
		<%{%> : block begin (default tab size 4)
		<%}%> : block end 
		Html code 
	Session handler
		http_handler.getSession(): session 
		http_handler : SimpleHTTPRequestHandler class

	files
		jsp, py, html, cs, image

	If only path is given
		oo.psp > oo.py > oo.html
source
	was.py : WEB Server 
	pspconfig.py : port, directory ... setup file
	gen.py : generator ps file to py 

	WEB/index.psp : sample psp  code
![index.jsp](./WEB/car/s.jpg)

install : git clone https://github.com/jangsooyoung/psp.git
setup   : cd psp
          editing pspconfig.py 
running : python3 was.py 

# psp
