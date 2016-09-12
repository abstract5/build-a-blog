import webapp2
import jinja2
import os
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    con = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("front.html", posts=posts)

class SubmitHandler(Handler):
    def render_submit(self, title="", con="", error=""):
        self.render("submit.html", title=title, con=con, error=error)

    def get(self):
        self.render_submit()

    def post(self):
        title = self.request.get("title")
        con = self.request.get("con")

        if title and con:
            p = Post(title=title, con=con)
            p.put()

            self.redirect("/")
        else:
            error = "We need both content and a title!"
            self.render_submit(title, con, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submission', SubmitHandler)#,
    #('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
