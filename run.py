#!venv/bin/python
import app
from app import webapp
if __name__ == '__main__':
	app.init()
	#app.webapp.run(host='127.0.0.1',debug=True)
	webapp.run(host='127.0.0.1')
