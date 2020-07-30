import re
import argparse
import os

tab = "\t"
linefeed = "\n"

def file_write(data):
    wf = open("tmp.py","a+")
    wf.write(data + linefeed)

def file_move(data):
    os.rename("tmp.py",data)

def static_write():
    file_write("import requests" + linefeed * 2 + "def req():")

def write_url(rawhost,rawuri,connection):
    uri = re.split(" ",rawuri.decode().rstrip())
    host = re.split(" ",rawhost.decode().rstrip())
    if connection == "http":
        file_write(tab + 'host = "http://' + host[1] + '"')
    else:
        file_write(tab + 'host = "https://' + host[1] + '"')
    file_write(tab + 'uri ="' + uri[1] + '"')

def write_headers(rawheaders):
    wdata = tab + "head ={" +linefeed
    headers_list = []
    length = len(rawheaders)
    for x in rawheaders:
        if not x.startswith(b"\r\n"):
            headers_list.append(x)
        else:
            break
    for x in headers_list:
        headers = re.split(": ",x.decode())
        wdata += tab * 2 + "'" + headers[0] + "':'" + headers[1].rstrip() + "'," + linefeed
    file_write(wdata[:-2] + linefeed + tab * 2 + "}" )

def req_write(method):
    wdata = tab +"response = "
    if method == "get":
        wdata += "requests.get(" + "host + uri," + "headers = head"
    elif method == "post":
        wdata += "requests.post(" + "host + uri," + "headers = head," + "data = contents"
    wdata += ")"
    file_write(wdata)
    response_write()

def response_write():
    file_write(tab + "print(response.text)" + linefeed * 2 + 'if __name__ == "__main__":' + linefeed + tab + "req()")
    
def post_req(contents):
    post_data = contents[len(contents)-1]
    wdata  = tab + "contents ={" + linefeed
    listcontent = re.split("&",post_data.decode())
    for x in listcontent:
         y = re.split("=",x.rstrip())
         wdata += (tab * 2 + "'" + y[0] + "':'" + y[1] + "'," + linefeed)
    wdata = wdata[:-2]
    wdata += "}"
    file_write(wdata)
    req_write("post")

def file_read(read_file,connection):
    read_file = open(read_file,"rb")
    contents = read_file.readlines()
    req_method = re.split(" ",contents[0].decode())
    static_write()
    rawuri = contents.pop(0)
    rawhost = contents.pop(0)
    write_url(rawhost,rawuri,connection)
    headers = write_headers(contents)
    if req_method[0] == "GET":
        req_write("get")
    elif req_method[0] == "POST":
        post_req(contents)

def arguments_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--input",required=True,help="input file")
    ap.add_argument("-o","--output",required=True,help="output file")
    ap.add_argument("-c","--connection",default="https",help="HTTP/HTTPS (default HTTPS)")
    args = vars(ap.parse_args())
    main(args["input"],args["output"],args["connection"])

def main(read_file,write_file,connection):
    file_read(read_file,connection)
    file_move(write_file)

if __name__ == "__main__":
    arguments_parse()
