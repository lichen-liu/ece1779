#!venv/bin/python
import user_app
from user_app import webapp
if __name__ == '__main__':
	#app.webapp.run(host='127.0.0.1',debug=True)
	webapp.run(host='127.0.0.1')
