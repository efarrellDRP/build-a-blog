#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os
import jinja2

from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape=True)

class Blog(db.Model):
    title = db.StringProperty( required = True )
    blog = db.TextProperty (required=True)
    created =db.DateTimeProperty (auto_now_add = True )
class Handler (webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class HomePage(Handler):
    def render_front (self,title="",blog="",link=""):
        blog_list=db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        self.render("homepage.html",title=title,blog=blog,blog_list=blog_list)
    def get(self):
        self.render_front()
    def post(self):
        title=self.request.get('title')
        blog=self.request.get('blog')
        if title and blog:
            b = Blog(title=title,blog=blog)

            b.put()

            self.redirect('/blog_list/{}'.format(b.key().id()))
        else:
            error="We need a title and blogpost!"
            self.render_list(title, blog, error)





class ViewPostHandler(Handler):
    def get(self, id_num):

        i=int(id_num)
        if Blog.get_by_id(i):

            k=Blog.get_by_id(i)
            title=k.title
            blog=k.blog

            self.render("single_blog.html",title=title,blog=blog)
        else:

            error="We need a valid id!"
            self.response.write(error)




app = webapp2.WSGIApplication([
    ('/', HomePage),webapp2.Route('/blog_list/<id_num:\d+>', ViewPostHandler)
], debug=True)
