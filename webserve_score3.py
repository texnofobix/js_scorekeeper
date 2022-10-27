from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
from getscores3 import get_all_team_scores,pretty_table

hostName = "0.0.0.0"
serverPort = 2999

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.write("<html><head><title>Juice Shop Team Score Totals</title></head>")
        self.write('<meta http-equiv="refresh" content="10">')
        self.write('<h1>Juice Shop Team Scores</h1>')
        #self.write("<p>Request: %s</p>" % self.path)
        self.write("<body>")
        # self.write("<p>This is an example web server.</p>")
        # self.write('<pre style="font-size: 18px">')
        self.write(str(pretty_table(get_all_team_scores(1,4))))
        self.write('\nas of {}'.format(datetime.datetime.now()))
        # self.write("</pre>")
        self.write("</body></html>")
    
    def write(self,string):
        return self.wfile.write(bytes(string, "utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")