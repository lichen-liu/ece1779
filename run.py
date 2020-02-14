#!venv/bin/python
import app

if __name__ == '__main__':
	app.init()
	#app.webapp.run(host='127.0.0.1',debug=True)
	app.webapp.run(host='127.0.0.1')