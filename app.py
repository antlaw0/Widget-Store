import os
from flask import Flask
from flask import render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email, password):
        self.name = name
        self.password=password
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description= db.Column(db.String(120))
    size= db.Column(db.String(12))
    color= db.Column(db.String(12))
	
    
    def __init__(self, name, description, size,color):
        self.name = name
        self.description=description
        self.size=size
        self.color=color
        
    def __repr__(self):
        return '<Name %r>' % self.name

		
def getId(email):
	u = User.query.filter_by(email=e).first()
	return u.id

def getUsername(email):
	u = User.query.filter_by(email=email).first()
	return u.name

	
def getPassword(email):
	u = User.query.filter_by(email=email).first()
	return u.password

	
		
def userExists(e):
	u = User.query.filter_by(email=e).first()
	if u == None:
		return False
	else:
		return True

		"""		
u= User(name, email, password)
db.session.add(u)
db.session.commit()
print("User: "+name+" created.")
"""
		
@app.route('/', methods=['POST', 'GET'])
def index():
    if 'email' in session:
        return render_template('store.html')
    else:
        messages=[]
        if request.method=='POST':
            
            email = request.form['email']
            password = request.form['password']
            #if entered email exists
            if userExists(email) == True:
                #if password matches password in database
                if getPassword(email) == password:
                    session['username']=getUsername(email)
                    session['email'] = email
                    return render_template('store.html', username=getUsername(email))

                else:
                    messages.append("Invalid password")
                    return render_template('index.html',  messages=messages)

            else:
                messages.append("User with that e-mail does not exist")
                return render_template('index.html', messages=messages)

        else:
           return render_template('index.html', messages=messages)
	

		

@app.route('/test', methods=['POST', 'GET'])
def test():
	
	#db.drop_all()
	#db.create_all()
	#u= User('Anthony', 'antlaw0@gmail.com', '12345678')
	#db.session.add(u)
	#db.session.commit()
	
	results=[]
	rs=User.query.all()
	results.append("Users \n")
	for r in rs:
		results.append(str(r.id)+" "+r.name+" "+r.email+" "+r.password)
	results.append(" \n Widgets")
	widgets=Widget.query.all()
	for i in widgets:
		results.append(str(i.id)+" "+i.name+" "+i.description+" "+i.size+" "+i.color)
	if request.method=='POST':
		name=request.form['name']
		description=request.form['description']
		size=request.form['size']
		color=request.form['color']
		w= Widget(name, description, size, color)
		db.session.add(w)
		db.session.commit()
		print("Widget: "+name+" added.")
		#return render_template('test.html', results=results)

	
	return render_template('test.html', results=results)

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    messages = []
    
    if request.method=='POST':
        email=request.form['email']
        username = request.form['username']
        password = request.form['password']
        password2=request.form['password2']
        #check if password and re-entered passwords match
        if password != password2:
            messages.append("Invallid password- passwords do not match. Please re-enter password")
            
        #check username length
        if len(username) < 1:
            messages.append("Invallid username")
        if len(username) > 20:
            messages.append("Invallid username- The entered username is too long. Usernames must be 20 characters or less in length.")
        
        #check password length
        if len(password) < 8:
            messages.append("Invallid password- passwords must be at least 8 characters long.")
        if len(password) > 20:
            messages.append("Invallid password- The password you entered is too long. Passwords must not be longer than 20 characters in length.")
        
        #if  error messages
        if len(messages) != 0:
            #return registration page with new error message(s)
            return render_template('registration.html', messages=messages)
        
        if userExists(email) == True:
            messages.append("User with that e-mail already exists")
            return render_template('registration.html', messages=messages)
        else:
            #insert new user
            u= User(username, email, password)
            db.session.add(u)
            db.session.commit()
	
            session['username'] = username
            session['email']=email
            return render_template('store.html')
    else:
        return render_template('registration.html', messages=messages)
    

			
#if __name__ == '__main__':
#port = int(os.environ.get('PORT', 5000))
#app.run(host='127.0.0.1', port=port, debug=True)
