Couchfy v0.2
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

In the directory _design, create your pattern. You can find an example in the directory _design.

In _design/build directory, are all compiled documents.

Run
----

For run:
```sh
python3 couchfy.py
```

If you want synchronize with CouchDB:
```sh
python3 couchfy.py -s sync
```
