from flask import Blueprint, request, g, jsonify, render_template, redirect, url_for
from app.db import get_db

TASK_LIST=[]

pages_bp = Blueprint('pages', __name__)


events_bp = Blueprint('events', __name__, url_prefix="/events")

@events_bp.route('/', methods=['GET'])
def event_page():
	events_list=get_all_events().get_json()
	context = {
		"message" : "all events",
		"events_list" : events_list
	}
	return render_template("event_page.html", **context)

@events_bp.route('/new_event', methods=['POST'])
def new_event():
	name = request.form['event-name']
	description = request.form['description']
	location = request.form['location']
	event_date = request.form['event-date']

	insert_cmd = "INSERT INTO events (event_name, description, location, event_date) VALUES (%s, %s, %s, %s)"
	val = (name, description,location,event_date)

	db = get_db()
	cursor = db.cursor()
	cursor.execute(insert_cmd,val)
	db.commit()
	cursor.close()
	return redirect(url_for("events.event_page"))


@events_bp.route('/get_all_events', methods=['GET'])
def get_all_events():
	db = get_db()
	cursor = db.cursor(dictionary=True)
	# cursor.execute("SELECT DATE(event_date) AS date_only, event_id, event_name, location, description FROM events")
	cursor.execute("SELECT * FROM events ORDER BY event_id DESC")
	events  = cursor.fetchall()
	cursor.close()
	return jsonify(events)


@events_bp.route('/delete_event/', methods=['POST'])
def delete_event():
	event_id = request.form['event_id_deletion']
	
	db = get_db()
	cursor = db.cursor()
	# cursor.execute("SELECT * FROM events WHERE event_id=%s", (str(event_id),))
	# queried_event = cursor.fetchall()
	
	cursor.execute("DELETE FROM events where event_id=%s",(str(event_id),))
	db.commit()
	cursor.close()
	
	return redirect(url_for("events.event_page"))



# -----------------------------------------------------------------------------------------------------

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route('/', methods=['GET'])
def task_page():

	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT event_id, event_name from events")
	events_list_dict = cursor.fetchall()
	tasks_dict = {}
	for event in events_list_dict:
		task_info = get_tasks_for_event(event['event_id'])
		tasks_dict[event['event_id']] = task_info
	
	task_list = []

	cursor.execute("SELECT task_id, task_name from tasks")
	task_id_list = cursor.fetchall()
	for task in task_id_list:
		task_id_name_pair=(task['task_id'], task['task_name'])
		task_list.append(task_id_name_pair)
	cursor.close()

	TASK_LIST = task_list

	context = {
		"message" : "tasks page",
		"events_list_dict" : events_list_dict,
		"tasks_dict" : tasks_dict,
		"task_list": task_list
	}

	return render_template('task_page.html', **context)



@tasks_bp.route("/new_task", methods=['POST'])
def new_task():
	event_id = request.form['select-event-id']
	name = request.form['task-name']
	deadline = request.form['task-deadline']
	status = request.form['task-status-selector']

	insert_cmd = "INSERT INTO tasks(event_id, task_name, deadline, status) VALUES (%s, %s, %s, %s)"
	val = (event_id,name, deadline, status)

	db = get_db()
	cursor = db.cursor()
	cursor.execute(insert_cmd, val)
	db.commit()
	cursor.close()
	return redirect(url_for("tasks.task_page"))


@tasks_bp.route("/get_tasks", methods=['GET'])
def get_tasks_for_event(event_id = None):
	if event_id is None:
		event_id = request.values['event_id']
	select_cmd = "SELECT * FROM tasks WHERE event_id=%s"
	val = (event_id,)

	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute(select_cmd, val)
	tasks = cursor.fetchall()
	cursor.close()
	return tasks

@tasks_bp.route("/update_task", methods=['POST'])
def update_task():
	task_status = request.form['task-status-update-selector']
	task_id = request.form['update-task-selector']
	update_cmd = "UPDATE tasks SET status=%s WHERE task_id=%s"
	val = (task_status, task_id)

	db = get_db()
	cursor = db.cursor()
	cursor.execute(update_cmd, val)
	db.commit()
	cursor.close()
	return redirect(url_for('tasks.task_page'))


#------------------------------------------------------------------------------------------------------------

attendees_bp = Blueprint("attendees", __name__, url_prefix="/attendees")


@attendees_bp.route('/', methods=['GET'])
def attendee_page():
	attendees_list = get_attendees()

	task_list = []
	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute("SELECT task_id, task_name from tasks")
	task_id_list = cursor.fetchall()
	for task in task_id_list:
		task_id_name_pair = (task['task_id'], task['task_name'])
		task_list.append(task_id_name_pair)
	cursor.close()

	context = {
		"message" : "Attendee page",
		"attendees_list" : attendees_list,
		"task_list" : task_list
	}
	return render_template('attendee_page.html', **context)


@attendees_bp.route("/add_attendee", methods=['POST'])
def add_attendee():
	attendee_name = request.form['attendee-name-input']
	insert_cmd = "INSERT INTO attendees (attendee_name) VALUES (%s)"
	val = (attendee_name,)


	db = get_db()
	cursor = db.cursor()
	cursor.execute(insert_cmd, val)
	db.commit()
	cursor.close()
	return redirect(url_for('attendees.attendee_page'))

@attendees_bp.route("/get_attendees", methods=['GET'])
def get_attendees():
	select_cmd = "SELECT * FROM attendees"

	db = get_db()
	cursor = db.cursor(dictionary=True)
	cursor.execute(select_cmd)
	attendees = cursor.fetchall()
	attendees_list = []
	for attendee in attendees:
		attendee_id_name_pair =(attendee['attendee_id'], attendee['attendee_name'])
		attendees_list.append(attendee_id_name_pair)
	return attendees_list

@attendees_bp.route("/delete_attendee", methods=['POST'])
def delete_attendee():
	attendee_id = request.form['remove-attendee-selector']
	
	db = get_db()
	cursor = db.cursor()
	delete_cmd = "DELETE FROM attendees WHERE attendee_id=%s" % (attendee_id,)
	cursor.execute(delete_cmd)
	db.commit()
	cursor.close()
	return redirect(url_for('attendees.attendee_page'))

@attendees_bp.route("/assign_attendee", methods=['POST'])
def assign_attendee():
	task_id = request.form['task-assignment']
	attendee_id = request.form['attendee-assignment']

	db = get_db()
	cursor = db.cursor(dictionary=True)

	cursor.execute('SELECT event_id FROM tasks WHERE task_id=%s',(task_id,))
	event_id = cursor.fetchone()['event_id']
	cursor.execute("INSERT INTO assignments (attendee_id, task_id, event_id) VALUES(%s, %s, %s)",(attendee_id, task_id, event_id))
	db.commit()
	cursor.close()
	return redirect(url_for('attendees.attendee_page'))