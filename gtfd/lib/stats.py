from datetime import datetime, timedelta

def getCompletionTimes(tasks):
	times = {"min": 0, "max": 0, "avg": 0, "tot": 0}
	task_count = 0
	for task in tasks:
		if task.done:
			task_count += 1
			time = round(task.completion_time().seconds/(3600.0), 2)
			if time > times['max']:
				times['max'] = time
			if time < times['min'] or times['min'] == 0:
				times['min'] = time
			times['tot'] += time
	if task_count:
		times['avg'] = round(times['tot']/task_count, 2)
	return times

def getStatsForMonth(tasks):
	start = (datetime.today()-timedelta(31)).date()
	end = datetime.today().date()
	days = {}
	current = start
	while current <= end: 
		days[current] = {}
		tasksForDay = [t for t in tasks if t.created.date()<=current]
		doneTasks = [t for t in tasksForDay if t.done]
		days[current]['done'] = len(doneTasks)
		days[current]['todo'] = len(tasksForDay) - days[current]['done']
		if len(tasksForDay) >= 1:
			days[current]['done_ratio'] = round((days[current]['done']*100)/float(len(tasksForDay)), 2)
			days[current]['todo_ratio'] = 100-days[current]['done_ratio']
		else:
			days[current]['done_ratio'] = 0 
			days[current]['todo_ratio'] = 0 
		days[current].update(getCompletionTimes(doneTasks))
		current += timedelta(1)
	return days

def getMonthTable(month, attributes):
	table = []
	for day in sorted(month):
		row = {"date": day,}
		for attribute in attributes:
			row[attribute] = month[day][attribute]
		table.append(row)
	return table


