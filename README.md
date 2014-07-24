Couchfy v0.3
=======

With Couchfy you can create a pattern for your application in CouchDB.

The tool enables build the design document and, as option, synchronize with database.

Dependencies
----
* CPython 3.3
* pycouchdb

Try it!
----

Download the Couchfy.

For install:
```sh
python3 setup.py install
```

In the directory _design, create your pattern. You can find an example in the directory example/_design.

You must create the configuration file "couchfy.config.json". A example in example/_design.

In _design/build directory, are all compiled documents.

Your project should look like this:
```sh
your_project/
	couchfy.config.json
	_design/
```

Run
----

For run:
```sh
python3 -m couchfy
```

If you want synchronize with CouchDB:
```sh
python3 -m couchfy -s sync
```
