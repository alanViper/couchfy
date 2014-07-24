import os, json, re, pycouchdb
from shutil import rmtree

DIR_APP_DOC = '_design'
DIR_APP_BUILD = '_design/build'

SERVER_COUCHDB = 'http://localhost:5984/'
COUCHDB_DB_NAME = 'test'


class Unify_design:
	"""
	Class for build the app to CouchDB.
	"""

	def __init__(self):
		global DIR_APP_DOC, DIR_APP_BUILD, SERVER_COUCHDB, COUCHDB_DB_NAME

		with open('couchfy.config.json', 'r') as config:
			config = json.loads(config.read())
			DIR_APP_DOC = config['DIR_DESIGN']
			DIR_APP_BUILD = config['DIR_BUILD']
			SERVER_COUCHDB = config['HOST']
			COUCHDB_DB_NAME = config['DATABASE']


	def _clear(self):
		"""
		Delete the directory of compilation.
		"""
		if os.path.exists(DIR_APP_BUILD):
			rmtree(DIR_APP_BUILD)


	def _list_docs(self, path):
		"""
		List recursively all documents in the directory.

		Return a dictionary that contains all the links to the documents.
		"""
		docs = []
		dir_list = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

		if len(dir_list) > 0:
			for dir_name in dir_list:
				for doc in self._list_docs(path+'/'+dir_name):
					docs.append(doc)

		list_files = [path+'/'+name for name in os.listdir(path) if name.endswith('.json')]

		if len(list_files) > 0:
			for doc_file in list_files:
				docs.append(doc_file)

		return docs


	def compiler(self):
		self._clear()
		docs = self._list_docs(DIR_APP_DOC)
		for doc in docs:
			with open(doc, 'r') as design_doc:
				design_doc = design_doc.read()
				try:
					obj_json = json.loads(design_doc)
					link = self._search_links(obj_json)
					if len(link) > 0:
						new_doc = self._unify(link, design_doc)
						doc_name = obj_json['_id'].replace('/', '-')
						self._save(doc_name+'.json', new_doc)
				except ValueError:
					print('File "%s" is empty or not JSON.' % (doc))


	def _search_links(self, doc, dic_link = {}):
		"""
		Search by links for javascript files.

		Parameter doc receives a document for seach.

		Return a dictionary that contains all the links.
		"""
		for key in doc:
			if type(doc[key]) is dict:
				self._search_links(doc[key], dic_link)
			elif type(doc[key]) is str:
				total_reference = len(doc[key])
				if doc[key][0:2] == '{{' and doc[key][(total_reference - 2):total_reference] == '}}':
					dic_link[doc[key]] = re.sub('[{{]|[}}]', '', doc[key])

		return dic_link


	def _unify(self, links, doc):
		"""
		links - Is a list of links for javascript files.
		doc - Document.

		Return the document with javascript compressed.
		"""
		for key in links:
			try:
				with open(DIR_APP_DOC+'/'+links[key], 'r') as js:
					doc = doc.replace(key, self._compress(js.read()))
			except FileNotFoundError:
				print('File "%s" not found.' % (links[key]))

		return doc


	def _compress(self, js):
		"""
		js - Javascript.
		"""
		js = re.sub('\n|\t', '', js)
		return js


	def _save(self, name, doc):
		"""
		name - The name of document.
		doc - Document.
		"""
		filename = DIR_APP_BUILD+'/'+name
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		with open(filename, 'w') as doc_file:
			doc_file.write(doc)
			doc_file.close()



class Couchdb_app:
	"""
	Synchronizes with CouchDB.
	"""

	def __init__(self):
		server = pycouchdb.Server(SERVER_COUCHDB)
		self.db = server.database(COUCHDB_DB_NAME)

	def update(self):
		if os.path.exists(DIR_APP_BUILD):
			docs = os.listdir(DIR_APP_BUILD)
			for doc in docs:
				with open(DIR_APP_BUILD+'/'+doc, 'r') as design_doc:
					design_doc = design_doc.read();
					design_doc = json.loads(design_doc)
					try:
						self.db.delete(design_doc['_id'])
					except pycouchdb.exceptions.NotFound:
						pass
					finally:
						self.db.save(design_doc)
