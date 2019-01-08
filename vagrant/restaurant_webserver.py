from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
restaurants = session.query(Restaurant).all()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Enter a new Restaurant: </h1>"
                output += """<form method ='POST' enctype='multipart/form-data' action='/restaurants/new'>
                          <input name='newRestaurantName' type='text'>
                          <input type='submit' value='Submit'></form>"""
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                restaurantID = self.path.split("/")[2]
                restaurantQuery = session.query(
                    Restaurant).filter_by(id=restaurantID).one()
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>Rename %s: </h1>" % restaurantQuery.name
                    output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantID
                    output += "<input name='editRestaurantName' type='text'>"
                    output += "<input type='submit' value='Submit'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode())
                    return

            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurantQuery = session.query(
                    Restaurant).filter_by(id=restaurantID).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>You are about to delete %s!!!" % restaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/delete'>" % restaurantID
                output += "<input type='submit' value='DELETE'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<h1><a href='/restaurants/new'>Add a New Restaurant Here.</a></h1>"
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<p>%s</p>" % restaurant.name
                    output += "<a href ='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br>"
                    output += "<a href = '/restaurants/%s/delete'>Delete</a>" % restaurant.id
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    newRestaurant = Restaurant(
                        name=messagecontent[0].decode())
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('editRestaurantName')

                    restaurantID = self.path.split("/")[2]
                    restaurantQuery = session.query(
                        Restaurant).filter_by(id=restaurantID).one()

                    if restaurantQuery != []:
                        restaurantQuery.name = content[0].decode()
                        session.add(restaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])

                restaurantID = self.path.split("/")[2]
                restaurantQuery = session.query(
                    Restaurant).filter_by(id=restaurantID).one()

                if restaurantQuery != []:
                    session.delete(restaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print('Web server is running on port %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == '__main__':
    main()
