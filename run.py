#!venv/bin/python
import app

#webapp.run(host='0.0.0.0',debug=True)
if __name__ == '__main__':
	app.init()
	#app.webapp.run(host='0.0.0.0')
	app.webapp.run(host='127.0.0.1')