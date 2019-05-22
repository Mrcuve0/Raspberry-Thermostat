from pymongo import MongoClient

DB_ADDRESS = '192.168.43.154' #'localhost'

client = MongoClient(DB_ADDRESS, 27017)
logs_collection = client['logs']
config_collection = client['new_coll']
test_collection = client['test']

def insert_log(log):
	posts = logs_collection.posts
	result = posts.insert(log)
	return result

def find_logs(criteria):
	posts = logs_collection.posts
	result = posts.find(criteria)
	return result

def get_configuration():
	posts = config_collection.posts
	config = posts.find_one()
	return config

def update_configuration(new_config):
	config = get_configuration()
	if config is not None:
		new_config['_id'] = config['_id']
	config_collection.posts.save(new_config)

# Some tests

update_configuration({'configa': 'prova'})
print(get_configuration())
update_configuration({'configa': 'sovrascritto'})
print(get_configuration())

print('    ')

elements = config_collection.posts.find()
for elem in elements:
	print(elem)
