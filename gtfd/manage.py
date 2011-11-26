from flaskext.script import Manager

from gtd import app
from gtd import mail
from gtd import conf 

from db import Task
from flaskext.mail import Message

manager = Manager(app)

@manager.command
def sendmail():
	task = Task.query.order_by(Task.created).first()
	msg = Message("Get things done!",
                  sender=("GTD", "gtd@gedankenacker.de"),
                  recipients=["ich@gedankenacker.de"])
	if not task:
		return
	msg.body = "Hey,\n how about doing '"+task.title+"'?\n"
	msg.body += "It has been waiting for "+task.waited_text()
	if task.postponed_count > 0:
		msg.body += " and you have postponed it "+str(task.postponed_count)+" already"
	msg.body += ".\n"
	msg.body += "Here is some more information:\n" 
	if len(task.desc.strip()) > 0:
		msg.body += "Description: "+task.desc_text()+"\n"
	if task.tags != "":
		msg.body += "Tags: "+task.tags+"\n"
	if task.due_text():
		msg.body += "Due: "+task.due_text()+"\n"
	if task.duration_text():
		msg.body += "Duration: "+task.duration_text()+"\n"
	if len(task.text.strip()) > 0:
		msg.body += "Text:\n"+task.text+"\n"
	msg.body += "\nMark task done: "+conf.SITE_URL+"do/"+str(task.id)+"/\n"
	msg.body += "Postpone to later: "+conf.SITE_URL+"postpone/"+str(task.id)+"/"
	print msg.body
	mail.send(msg)

if __name__ == "__main__":
    manager.run()
