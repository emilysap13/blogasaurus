import webapp2
import os
import jinja2
from models import Post
from models import Author



#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('my_blog.html')
        self.response.write(template.render())

class AboutMeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('about_me.html')
        self.response.write(template.render())

class PostsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template('posts.html')
        self.response.write(template.render())

    def post(self):


#        username = self.request.get('username')
        post_title = self.request.get('post_title')
        post_content = self.request.get('post_content')
        tags = self.request.get('tags')
        username_input = self.request.get('username')

        #if len(basic_post == 0):
        #    new_author = models.Author(username=username, posts=posts)

        #basic_post_title = basic_post.post_title
        #basic_post_content = basic_post.post_content

        basic_post = Post(post_title=post_title, post_content=post_content, tags=tags)
#        if models.Author.query(Author.username == username):
#            author = models.Author.query(Author.username).get()
        basic_post_key = basic_post.put()

        check_authors = Author.query(Author.username == username_input).fetch()
        #check_authors=[Author(username, post)]
        if len(check_authors) > 0:
            author = check_authors[0] #check_authors returns a list - get first item (name of author!)
            author.posts.append(basic_post_key)
        else:
            author = Author(username=username_input, posts=[basic_post_key])

        author.put()

        blog_posts = []
        for basic_post_key in author.posts:
            blog_posts.append(basic_post_key.get())
        template_vars = {
            'username': username_input,
            'tagslist': tags.split(','),
            # 'post_title': post_title,
            # 'post_content': post_content
            'blog_posts': blog_posts
        }

    #    template = jinja_current_dir.get_template('show_post.html')
    #    self.response.write(template.render(template_vars))
        template = jinja_current_dir.get_template('showmanyposts.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aboutme', AboutMeHandler),
    ('/posts', PostsHandler),
], debug=True)
