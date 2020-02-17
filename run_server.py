#!venv/bin/python
import app
from app import webapp
if __name__ == '__main__':
	app.init()
	webapp.run(host='0.0.0.0')
