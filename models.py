def userExists(name):
	u = User.query.filter_by(name='John Smith').first()
	if u == None:
		return False
	else:
		return True