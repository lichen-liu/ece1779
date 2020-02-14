#!venv/bin/python
import app

if __name__ == '__main__':
	app.init()
	app.webapp.run(host='0.0.0.0')