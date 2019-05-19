from pymongo import MongoClient

DB_ADDRESS = '192.168.43.154' #'localhost'

client = MongoClient(DB_ADDRESS, 27017)
logs_collection = client['logs']
config_collection = client['config']

def insert_log(log):
	posts = logs_collection.posts
	result = posts.insert(log)
	return result

def find_log(criteria):
	posts = logs_collection.posts
	result = posts.find_one(criteria)
	return result

def get_configuration():
	pass

def get_last_temperatures():
	pass



#
#post_data = {
#	'title': 'Prova',
#	'content': 'sto a prova'
#}
#result = posts.insert(post_data)
#
#print(posts.find_one({'title': 'Prova'}))
