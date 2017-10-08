from flask import Flask, render_template, flash, session, redirect, request
import models as dbHandler
import os
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
	message=None
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		#if entered username exists
		if dbHandler.userExists(username) == True:
			#if password matches password in database
			if dbHandler.getPassword(username) == password:
				return render_template('store.html', username=username)
			else:
				message="Invalid password"
				return render_template('index.html', message=message)		
        
		else:	   
			message="User does not exist"
			return render_template('index.html', message=message)		
        
	else:
		return render_template('index.html', message=message)
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	message=None
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		if dbHandler.userExists(username) == True:
			message="UserAlready exists"
			return render_template('signup.html', message=message)
		else:
			#insert new user
			dbHandler.insertUser(username, password)
			return render_template('store.html', username=username)
                               
	else:
		return render_template('signup.html', message=message)
    
@app.route('/store', methods=['GET', 'POST'])
def store():
	if not session.get('logged_in'):
		return "You do not have access to this page"
	else:
		return render_template('store.html', username=username)
    


if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)