from flask import Flask, render_template
from app.db import init_db
from app.db import close_db

from app.routes import events_bp
from app.routes import tasks_bp
from app.routes import attendees_bp

def create_app():
	app = Flask(__name__)
	app.config.from_object("app.config.Config")

	init_db(app)

	@app.route('/', methods=['GET'])
	def main():
		context = {
			"message" : "landing page"
		}
		return render_template('base.html', **context)

	app.register_blueprint(events_bp)
	app.register_blueprint(tasks_bp)
	app.register_blueprint(attendees_bp)

	# app.teardown_appcontext(close_db)
	
	return app