from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta
from conf import DB_URL
from werkzeug import secure_filename
from functions import fuzzy_delta
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import re

cal = pdc.Constants("de")
engine = create_engine(DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Content(Base):
    __tablename__ = "contents"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    page = Column(String(50))
    html = Column(Text)
    created = Column(DateTime, default=datetime.now())
    def __init__(self, page=None, html=None):
        self.page = page
        self.html = html 

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    text = Column(Text)
    desc = Column(Text)
    created = Column(DateTime, default=datetime.now())
    postponed_date = Column(DateTime, default=datetime.now())
    postponed_count = Column(Integer, default=0)    
    important = Column(Boolean, default=False)
    done = Column(Boolean, default=False)
    done_date = Column(DateTime)
    due_date = Column(DateTime)
    duration = Column(Integer, default=0)
    tags = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('tasks', lazy='dynamic'))

    def __init__(self, user_id, text="", desc=""):
        self.user_id = user_id
        self.text = text 
        self.desc = desc
        self.update()

    def get_tags(self):
        return sorted(map(str.lower, re.findall("#(\w+)", self.desc)))
    
    def desc_text(self):
        noopts = re.sub("([@~#][^@~#]+)", "", self.desc).strip()
        if noopts.startswith("!"):
            noopts = noopts[1:]
        return noopts

    def get_duration(self):
        dur = re.search("~(.*?)($|#|@|~)", self.desc)
        if dur:
            dur = dur.group(1).strip()
            absolute = pdt.Calendar(cal).parse(dur)
            relative = datetime(*absolute[0][:6])-datetime.now()
            return relative.days*24*3600+relative.seconds
        return 0
    
    def duration_text(self):
        if self.duration <= 0:
            return None
        delta = timedelta(0, self.duration)
        return fuzzy_delta(delta)

    def get_due(self):
        due = re.search("@(.*?)($|#|@|~)", self.desc)
        if due:
            due = due.group(1).strip()
            absolute = pdt.Calendar(cal).parse(due)
            return datetime(*absolute[0][:6])
        return None

    def due_text(self):
        if not self.due_date:
            return None
        delta = self.due_date-datetime.now()
        if delta > timedelta(1):
            return "on "+str(self.due_date)
        return "in "+fuzzy_delta(delta)

    def is_important(self):
        return self.desc.startswith("!")

    def update(self):
        self.duration = self.get_duration()
        self.due_date = self.get_due()
        self.title = self.desc_text()
        self.tags = '#'.join(self.get_tags())
        self.important = self.is_important()
        if len(self.tags.strip()) > 0:
            self.tags = "#"+self.tags
    
    def completion_time(self):
        return datetime.now()-self.created

    def waited_text(self):
        return fuzzy_delta(self.completion_time())
    
    def complete(self):
        self.done = True
        self.done_date = datetime.now()

    def uncomplete(self):
        self.done = False
        self.done_date = None

    def postpone(self):
        self.postponed_count += 1
        self.postponed_date = datetime.now()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(200))
    notify = Column(Boolean, default=False)

    def __init__(self, name, email=""):
        self.name = name
        self.email = email

class Auth(Base):
    __tablename__ = 'auths'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    auth = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('auths', lazy='dynamic'))

    def __init__(self, auth, uid):
        self.auth = auth
        self.user_id = uid

def init_db():
    Base.metadata.create_all(bind=engine)
