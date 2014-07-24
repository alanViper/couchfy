from .couchfy import Unify_design, Couchdb_app
import os

CONFIG_FILE = 'couchfy.config.json'


def couchdb_sync():
	couch = Couchdb_app()
	couch.update()


def config_file_exists():
	files = os.listdir('.')
	if not CONFIG_FILE in files:
		print("\nERROR: Config file not found.\n")
		return False
	else:
		return True


from optparse import OptionParser
parser = OptionParser()
parser.add_option('-s', '--sync', dest='sync')
if config_file_exists():
	opts = parser.parse_args()
	opts = opts[0]
	unify = Unify_design()
	unify.compiler()
	if opts.sync == 'sync':
		couchdb_sync()
