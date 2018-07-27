from google.appengine.ext import ndb



class Post(ndb.Model):
    post_title = ndb.StringProperty()
    post_content = ndb.TextProperty()
    # username = ndb.StringProperty()
    tags = ndb.StringProperty()

class Author(ndb.Model):
    username = ndb.StringProperty()
    posts = ndb.KeyProperty(kind="Post", repeated=True)
