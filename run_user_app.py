#!venv/bin/python
import user_app
from user_app import webapp
if __name__ == '__main__':
	webapp.run(host='0.0.0.0')
