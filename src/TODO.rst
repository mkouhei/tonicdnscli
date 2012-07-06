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
* Check specifying priority with creating MX|SRV record.
* Reduce step of creating zone. Current step is below:

  #. create template for new zone
  #. create zone
  #. delete template or update template for next new zone

  * Used template is unable to re-use directly
  * I will migrate these steps to 1 step

Known bug
---------

* When using in preference --config option than $HOME/.tdclirc.
