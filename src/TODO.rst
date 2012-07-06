ToDo
====

Features
--------

* Checking existing records When create or delete records.
* Updating records.
* Validation input data.

Improvement
-----------

* Add unittest.
* Use option '--domain' when bulk_create and bulk_delete.
* Specify timeout value.
* Change minimock to Mock for being compatible Python2.7 and Python3.2.

Known bug
---------

* When using in preference --config option than $HOME/.tdclirc.
* Unable to change MNAME,RNAME in SOA record.
