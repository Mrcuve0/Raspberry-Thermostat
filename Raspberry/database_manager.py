from pymongo import MongoClient

class database_manager:
	DB_ADDRESS = 'localhost'
	logs_collection = None
	config_collection = None
	roomData_collection = None
	temperatures_collection = None
	test_collection = None
	client = None
	db = None

	def __init__(self):
		self.client = MongoClient(self.DB_ADDRESS, 27017)
		self.db = self.client['thermodb']
		self.logs_collection = self.db['logs_coll']
		self.config_collection = self.db['config_coll']
		self.roomData_collection = self.db["roomData_coll"]
		self.temperatures_collection = self.db['temp_coll']
		self.test_collection = self.db['test']

	def insert_log(self, log):
		result = self.logs_collection.insert(log)
		return result

	def update_log(self, log):
		log['flag'] = 1
		result = self.logs_collection.save(log)
		return result

	def find_logs(self, criteria):
		result = self.logs_collection.find(criteria)
		return result

	def get_configuration(self):
		return self.config_collection.find_one()

	def update_configuration(self, new_config):
		config = self.get_configuration()
		if config is not None:
			new_config['_id'] = config['_id']
		self.config_collection.save(new_config)

	def get_roomData_configuration(self):
		return self.roomData_collection.find_one()

	def update_roomData_configuration(self, new_roomData_config):
		roomData_config = self.get_roomData_configuration()
		if roomData_config is not None:
			new_roomData_config["_id"] = roomData_config["_id"]
		self.roomData_collection.save(new_roomData_config)

	def get_last_temperatures(self):
		result = self.temperatures_collection.find_one()
		if result is not None:
			return result['list'] 
		return result

	def update_last_temperatures(self, new_list):
		new_item = {'list': new_list}
		item = self.temperatures_collection.find_one()
		if item is not None:
			new_item['_id'] = item['_id']
		self.temperatures_collection.save(new_item)

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
