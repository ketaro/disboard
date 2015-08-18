from app import db
from app.helpers import hash_password
import forgery_py


class User(db.Model):
    __tablename__ = 'users'
    
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(120), index=True, unique=True, nullable=False)
    givenname   = db.Column(db.String(30))
    surname     = db.Column(db.String(30))
    password    = db.Column(db.String(200))     # hash
    tos_agree   = db.Column(db.Integer)         # epoch datetime
    verified    = db.Column(db.Integer)         # epoch datetime, verified email address
    last_login  = db.Column(db.Integer)         # epoch datetime
    created_at  = db.Column(db.Integer,     nullable=False)         # epoch datetime
    created_by  = db.Column(db.String(120), nullable=False)
    updated_at  = db.Column(db.Integer,     nullable=False)         # epoch datetime
    updated_by  = db.Column(db.String(120), nullable=False)
    
    
    def __repr__(self):
        return '<User %r (%d)>' % (self.email, self.id)
    
    # For Flask-Login
    def is_authenticated(self):
        return True
    
    # For Flask-Login
    def is_active(self):
        return True
    
    # For Flask-Login
    def is_anonymous(self):
        return False
    
    # Admin users have access to the manager view
    def is_admin(self):
        return True
    
    # For Flask-Login
    def get_id(self):
        return unicode(self.id)

    def last_first(self):
        return ", ".join([self.surname, self.givenname])

    def first_last(self):
        return " ".join([self.givenname, self.surname])



class Category(db.Model):
    __tablename__ = 'categories'
    
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), index=True, nullable=False)
    
    questions   = db.relationship('Question', backref='category', order_by='Question.order_id')

class Question(db.Model):
    __tablename__ = 'questions'
    
    id          = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True, nullable=False)
    status      = db.Column(db.Enum('active', 'inactive'), default='active', nullable=False)
    title       = db.Column(db.String(50))
    order_id    = db.Column(db.Integer, default=0)
    
    slides      = db.relationship('Slide', backref='question', order_by='Slide.order_id')


class Slide(db.Model):
    __tablename__ = 'slides'
    
    id          = db.Column(db.Integer, primary_key=True)
    slide_type  = db.Column(db.Enum('title', 'text', 'choice', 'video'), default='text', nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    order_id    = db.Column(db.Integer, default=0)
    content     = db.Column(db.Text())
    prompt      = db.Column(db.String(1000))
    
    
    @property
    def hashdata(self):
        r = {
            'slide_id':   self.id,
            'slide_type': self.slide_type,
            'content':    self.content,
            'prompt':     self.prompt,
            'order_id':   self.order_id
        }
        
        return r
