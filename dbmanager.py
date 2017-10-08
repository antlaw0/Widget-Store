import sqlite3
import models as dbhelper

def create_database():
	sqlite_file = 'database.db'    # name of the sqlite database file
	table_name = 'users'	# name of the table to be created
	id_column='id_column'

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	# Creating a new SQLite table 
	c.execute('CREATE TABLE {tn} ({nf} {ft})'\
			.format(tn=table_name, nf=id_column, ft='INTEGER PRIMARY KEY AUTOINCREMENT'))

	#add next column
	new_column='username'
	column_type='TEXT'
	c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
			.format(tn=table_name, cn=new_column, ct=column_type))

	#add next column
	new_column='password'
	column_type='TEXT'
	c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
			.format(tn=table_name, cn=new_column, ct=column_type))
	
	print("Database and table created")

	# Committing changes and closing the connection to the database file
	conn.commit()

def show_entries():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()

	c.execute("SELECT * FROM users")
	print(c.fetchall())

running=True
print("Database Manager running. Type show to see the database, create to recreate the database, and exit to stop the manager.")
while(running==True):
	cmd=input("Enter command: ")
	if cmd == "show":
		show_entries()
	elif cmd == "exists":
		n=input("Enter username to query if exists: ")
		dbhelper.userExists(n)
	elif cmd == "create":
		create_database()
	elif cmd == "password":
		n=input("Enter username to get password for: ")
		p= dbhelper.getPassword(n)
		
		if dbhelper.getPassword(n)== '12345':
			print('success')
		else:
			print("no")
			#print(dbhelper.getPassword(n))
	elif cmd=="insert":
		dbhelper.insertUser("Anthony","12345")
		print("User inserted")
	else:
		print("Exiting...")
		running=False
		break;