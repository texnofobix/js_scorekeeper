from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import datetime

hostName = "0.0.0.0"
serverPort = 2999


def get_team_score(team_number):
    port = "3{}".format(str(team_number).rjust(3, '0')) # pad team number as 3XXX
    url = "http://127.0.0.1:{}/api/Challenges".format(port)

    try:
        with urllib.request.urlopen( url) as response:
            html = response.read()
            challenge_data = json.loads(html)
            total_points  = 0
            earned_points = 0

            for challenge in challenge_data['data']:
                # disabledEnv Might need to ignore "Docker"

                if challenge['disabledEnv'] != 'Docker':
                    total_points += challenge['difficulty']
                    
                    if challenge['solved']:
                        earned_points += challenge['difficulty']
            
            return 'Team {}: {}/{}'.format(team_number, earned_points, total_points)
    except urllib.error.URLError:
        return 'Team {}: {}'.format(team_number, 'no response') 

def get_all_team_scores(start,end):
    response = ""
    for team_number in range(1, end + 1):
        response += str(get_team_score(team_number)) + "\n"
    return response


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
        self.write('<pre style="font-size: 18px">')
        self.write(get_all_team_scores(1,4))
        self.write('as of {}'.format(datetime.datetime.now()))
        self.write("</pre>")
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