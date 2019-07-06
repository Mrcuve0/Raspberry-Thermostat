from pymongo import MongoClient

class database_manager
	DB_ADDRESS = '192.168.43.154' #'localhost'
	logs_collection = client['logs']
	config_collection = client['new_coll']
	temperatures_collection = client['tempe_coll']
	test_collection = client['test']
	client = None

	def __init__(self):
		client = MongoClient(DB_ADDRESS, 27017)

	def insert_log(log):
		posts = logs_collection.posts
		result = posts.insert(log)
		return result

	def update_log(log):
		log['flag'] = 1
		posts = logs_collection.posts
		result = posts.save(log)
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

	def get_last_temperatures():
		posts = temperatures_collection.posts
		item = posts.find_one()
		return item

	def update_last_temperatures(new_item):
		item = get_last_temperatures()
		if item is not None:
			new_item['_id'] = item['_id']
		temperatures_collection.posts.save(new_item)

# Some tests
# db = database_manager()
# db.update_configuration({'configa': 'prova'})
# print(db.get_configuration())
# db.update_configuration({'configa': 'sovrascritto'})
# print(db.get_configuration())

# print('    ')

# elements = db.config_collection.posts.find()
# for elem in elements:
# 	print(elem)
