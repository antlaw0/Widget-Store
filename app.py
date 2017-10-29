import os
from flask import Flask
from flask import render_template, session, request, redirect, url_for, flash
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
    type = db.Column(db.String(120))


    def __init__(self, name, email, password,type):
        self.name = name
        self.password=password
        self.email = email
        self.type=type

    def __repr__(self):
        return '<Name %r>' % self.name

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description= db.Column(db.String(120))
    size= db.Column(db.String(12))
    color= db.Column(db.String(12))
    price = db.Column(db.Integer)
    
	
    
    def __init__(self, name, description, size,color, price):
        self.name = name
        self.description=description
        self.size=size
        self.color=color
        self.price=price
        
    def __repr__(self):
        return '<Name %r>' % self.name

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    itemid = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(120))


    def __init__(self, userid, itemid, quantity, status):
        self.userid=userid
        self.itemid=itemid
        self.quantity=quantity
        self.status=status
		
    def __repr__(self):
        return '<Name %r>' % self.name

		
		
def getId(e):
	u = User.query.filter_by(email=e).first()
	return u.id

def getUsername(email):
	u = User.query.filter_by(email=email).first()
	return u.name

def getAccountType(email):
	u = User.query.filter_by(email=email).first()
	return u.type

def getWidgets():
	mainList=[]
	rs=Widget.query.all()
	for r in rs:
		l=[]
		l.append(r.id)
		l.append(r.name)
		l.append(r.description)
		l.append(r.size)
		l.append(r.color)
		l.append(format(r.price/100, '.2f'))
		mainList.append(l)
		#widgets.append(r.name+" "+r.description+" "+r.size+" "+r.color+" "+r.price)
	return mainList
		
	
def getPassword(email):
	u = User.query.filter_by(email=email).first()
	return u.password

def getOrdersById(i):
	mainList=[]
	rs=Order.query.all()
	for r in rs:
		if r.userid == i:
			l=[]
			l.append(r.id)
			l.append(r.itemid)
			#get name of widget in order
			w = Widget.query.filter_by(id=r.itemid).first()
			#put widget name in order list
			l.append(w.name)
			l.append(r.quantity)
			l.append(r.status)
			mainList.append(l)
		
	return mainList
	
		
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
        return render_template('store.html', username=session['username'], widgets=getWidgets(), orders=getOrdersById(session['id']))
    else:
        messages=[]
        if request.method=='POST':
            
            email = request.form['email']
            password = request.form['password']
            #if entered email exists
            if userExists(email) == True:
                #if password matches password in database
                if getPassword(email) == password:
                    session['id']=getId(email)
                    session['username']=getUsername(email)
                    session['email'] = email
                    session['accounttype']=getAccountType(email)
                    username=session['username']
                    return render_template('store.html', username=username, widgets=getWidgets(), orders=getOrdersById(session['id']))

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
	if 'accounttype' in session:
		if session['accounttype'] != 'admin':
			return render_template('index.html',messages=None)
	
	
	#i=1
	#w = Widget.query.filter_by(id=i).first()
	#w.size='gigantic'
	#db.session.commit()
	
	#db.drop_all()
	#db.create_all()
	#u= User('Anthony', 'antlaw0@gmail.com', '12345678')
	#db.session.add(u)
	#db.session.commit()
	
	
	results=[]
	rs=User.query.all()
	results.append("Users \n")
	for r in rs:
		results.append(str(r.id)+" "+r.name+" "+r.email+" "+r.password+" "+r.type)
	results.append(" \n Widgets")
	widgets=Widget.query.all()
	for i in widgets:
		results.append(str(i.id)+" "+i.name+" "+i.description+" "+i.size+" "+i.color+" "+"$"+str(format(i.price/100,'.2f')))
	orders=Order.query.all()
	results.append("\n Orders \n Order ID userID itemID Quantity order status")
	for o in orders:
		results.append(str(o.id)+" "+str(o.userid)+" "+str(o.itemid)+" "+str(o.quantity)+" "+o.status)
	if request.method=='POST':
		id=request.form['id']
		name=request.form['name']
		description=request.form['description']
		size=request.form['size']
		color=request.form['color']
		price=request.form['price']
		delete=request.form['delete']
		userid=request.form['userid']
		username=request.form['username']
		email=request.form['email']
		password=request.form['password']
		accounttype=request.form['accounttype']
		userdelete=request.form['userdelete']
		print("form to create new widget submitted.")
		#if userid submitted
		if userid != "":
			u = User.query.filter_by(id=userid).first()
			if username != "":
				u.name=username
			if email != "":
				u.email=email
			if password != "":
				u.password=password
			if accounttype != "":
				u.type=accounttype
			db.session.commit()
		
		
		#no id specified, create new widget
		if id == "":
			if name != "" and description !="" and size !="" and color != "" and price != "":
				w= Widget(name, description, size, color, price)
				db.session.add(w)
				db.session.commit()
				print("Widget: "+name+" added.")
				return render_template('test.html', results=results)

			else:
				flash("enter all fields")
		else:	
			w = Widget.query.filter_by(id=id).first()
			#if delete checkbox checked, delete widget with given id
			if delete =="delete":
				db.session.delete(w)
				db.session.commit()
				return render_template('test.html', results=results)
			if name != "":
				w.name=name
			if description != "":
				w.description=description
			if size != "":
				w.size=size
			if color != "":
				w.color=color
			if price != "":
				w.price=price
			db.session.commit()
			return render_template('test.html', results=results)

		return render_template('test.html', results=results)

	
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
            u= User(username, email, password,'customer')
            db.session.add(u)
            db.session.commit()
	
            session['username'] = username
            session['email']=email
            session['id']=getId(email)
            return render_template('store.html', username=username, widgets=getWidgets(), orders=getOrdersById(session['id']))
    else:
        return render_template('registration.html', messages=messages)
    
@app.route('/store', methods=['POST', 'GET'])
def store():
	if 'email' in session:
		if request.method == 'POST':
			i=request.form['wid']
			w = Widget.query.filter_by(id=i).first()
			wid=w.id
			widgetName=w.name
			widgetDescription=w.description
			widgetSize=w.size
			widgetColor=w.color
			widgetPrice=format(w.price/100,'.2f')
			return render_template('viewWidget.html', wid=wid, widgetName=widgetName, widgetDescription=widgetDescription, widgetSize=widgetSize, widgetColor=widgetColor, widgetPrice=widgetPrice)
	
		widgets=getWidgets()
		orders=getOrdersById(session['id'])
		return render_template('store.html', username=session['username'], widgets=widgets, orders=orders)
	else:
		messages=[]
		messages.append("log in to continue")
		return render_template('index.html', messages=messages)
	
@app.route('/viewWidget', methods=['POST', 'GET'])
def viewWidget():
	if 'email' in session:
		i=request.form['wid']
		if request.method == 'POST':
			i=request.form['wid']
			quantity=request.form['quantity']
			uid=session['id']
			#print("UserID is "+str(uid)+" WidgetID is "+i+" and quantity is "+quantity)
			#Add order to Order table
			o= Order(uid, i, quantity, 'open')
			db.session.add(o)
			db.session.commit()
			#go back to store
			return render_template('store.html', username=session['username'], widgets=getWidgets(), orders=getOrdersById(session['id']))
	

		w = Widget.query.filter_by(id=i).first()
		wid=w.id
		widgetName=w.name
		widgetDescription=w.description
		widgetSize=w.size
		widgetColor=w.color
		widgetPrice=w.price
		
		return render_template('viewWidget.html', wid=wid, widgetName=widgetName, widgetDescription=widgetDescription, widgetSize=widgetSize, widgetColor=widgetColor, widgetPrice=widgetPrice)
	
	else:
		messages=[]
		messages.append("log in to continue")
		return render_template('index.html', messages=messages)
	
			
#if __name__ == '__main__':
#port = int(os.environ.get('PORT', 5000))
#app.run(host='127.0.0.1', port=port, debug=True)
