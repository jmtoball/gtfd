from datetime import datetime, timedelta
from flask import url_for, request, redirect, flash, session, g
from gtfd.site import app
from gtfd.lib import stats
from gtfd.db import db_session, Task, User
from gtfd.views.common import render

@app.route('/', methods=["POST", "GET"])
@app.route('/tag/<tag>/', methods=["POST", "GET"])
@app.route('/edit/<edit_id>/')
def home(action=None, tag=None, edit_id=None):
	if not g.user:
		return redirect(url_for("login"))
	edit = None
	template = "home.html"
	task_qry = g.user.tasks
	tasks = task_qry
	#FIXME: WTF, this must be refactored soon
	task = task_qry.order_by(Task.postponed_date, Task.created).filter(Task.done==False).filter(Task.postponed_date<=datetime.today()-timedelta(2))
	if tag:
		tasks = tasks.filter(Task.tags.like('%#'+tag+'%'))
		task = task.filter(Task.tags.like('%#'+tag+'%'))
	if edit_id:
		edit = Task.query.filter(Task.id==edit_id).first()
	task = task.first()
	return render(template, tasks=tasks, task=task, edit=edit)

@app.route('/dotoggle/<id>/')
def do(id):
	task = Task.query.filter(Task.id==id).first()
	if task.done:
		task.uncomplete()
		flash("Task undone - Wait, how is this even possible?!")
	else:
		task.complete()
		flash("Task done - That was fucking awesome, you rock!")
	db_session.merge(task)
	db_session.commit()
	return redirect(url_for("home"))

@app.route('/postpone/<id>/')
def postpone(id):
	task = Task.query.filter(Task.id==id).first()
	task.postpone()
	db_session.merge(task)
	db_session.commit()
	flash("Task postponed - You can't postpone forever!")
	return redirect(url_for("home"))

@app.route('/delete/<id>/')
def delete(id):
	task = Task.query.filter(Task.id==id).first()
	db_session.delete(task)
	db_session.commit()
	flash("Task deleted - Failed to delete conscience")
	return redirect(url_for("home"))

@app.route('/edit/<id>/', methods=["POST"])
def edit(id):
	task = Task.query.filter(Task.id==id).first()
	data = request.form
	task.text = data['text'] 
	task.desc = data['desc'] 
	task.update()
	db_session.merge(task)
	db_session.commit()
	flash("Task updated - Succesfully made it more challenging!")
	return redirect(url_for("home"))

@app.route('/startoggle/<id>/')
def startoggle(id):
	task = Task.query.filter(Task.id==id).first()
	if task.desc.startswith("!"):
		task.desc = task.desc[1:]
	else:
		task.desc = "!"+task.desc
	task.update()
	db_session.merge(task)
	db_session.commit()
	if task.desc.startswith("!"):
		flash("Task Starred - Finally recognized it as important")
	else:
		flash("Task Unstarred - now marked as supposedly unimportant")
	return redirect(url_for("home"))

@app.route('/new/', methods=["POST"])
def new():
	data = request.form
	task = Task(g.user.id, data['text'], data['desc'])
	print(task)
	db_session.add(task)
	db_session.commit()
	flash("Task added - Yet more to do, awesome!")
	return redirect(url_for("home"))

@app.route('/statistics/')
def statistics():
	tasks = g.user.tasks
	statistics = {}
	statistics['tasks'] = tasks.count()
	statistics['tasks done'] = tasks.filter_by(done=True).count()
	statistics['tasks todo'] = tasks.filter_by(done=False).count()
	month = stats.getStatsForMonth(tasks)
	todo_done_table = stats.getMonthTable(month, ["todo", "done"])
	todo_ratio_table = stats.getMonthTable(month, ["todo_ratio", "done_ratio"])
	time_table = stats.getMonthTable(month, ["min", "max", "avg", "tot"])
	return render("stats.html", stats=statistics, todo_done_table=todo_done_table, todo_ratio_table=todo_ratio_table, time_table=time_table)	

