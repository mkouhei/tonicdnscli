History
-------

0.10 (2013-04-01)
^^^^^^^^^^^^^^^^^

* Change format of pretty print
* move test directory

0.9 (2012-09-13)
^^^^^^^^^^^^^^^^

* Refine search
* Update single record

0.8.4 (2012-09-12)
^^^^^^^^^^^^^^^^^^

* Fix typo

0.8.3 (2012-09-12)
^^^^^^^^^^^^^^^^^^

* Fix bug local variable 'auto_update_soa' referenced before assignment without update_soa flag

0.8.2 (2012-09-11)
^^^^^^^^^^^^^^^^^^

* Fix bug local variable 'auto_update_soa' referenced before assignment

0.8.1 (2012-09-11)
^^^^^^^^^^^^^^^^^^

* Add updating SOA serial automatically
* Fix travic-ci runnning error of test_pep8
* Refacotoring

  * Change method name
  * Remove unnecessary method, module

0.8 (2012-07-08)
^^^^^^^^^^^^^^^^

* Add Creating zone

  * Sub-command 'zone_create'
  * Support MASTER, SLAVE, NATIVE
  * execute next process:

    #. creating template
    #. creating zone
    #. deleting template

* Remove template_create_update sub-command
* Add Deleting zone

  * Sub-command 'zone_delete'

* Add options of soa sub-command
* Add option '--domain' to bulk_create, bulk_delete sub-commands

0.7.1 (2012-06-29)
^^^^^^^^^^^^^^^^^^

* Fix bug module import
* Fix bug that assert is always true of test_pep8

0.7 (2012-06-29)
^^^^^^^^^^^^^^^^

* Add default timeout
* Update unit tests
* Tool of adding user account of TonicDNS

0.6.2 (2012-06-17)
^^^^^^^^^^^^^^^^^^

* New feature of getting all zones
* Add pre-commit hook script
* Rename method name that test_getJSON to test_setJSON
* Refactoring of http connect

0.6.1.1 (2012-05-23)
^^^^^^^^^^^^^^^^^^^^

* Fix README

0.6.1 (2012-05-23)
^^^^^^^^^^^^^^^^^^

* Fix issue#2
* Refactoring

0.6 (2012-05-15)
^^^^^^^^^^^^^^^^

* Update SOA

0.5.2 (2012-05-11)
^^^^^^^^^^^^^^^^^^

* create or delete a specific record

0.5.1 (2012-05-07)
^^^^^^^^^^^^^^^^^^

* Fix bug get fail when resolver is SLAVE

0.5 (2012-05-04)
^^^^^^^^^^^^^^^^

* templates CRUD

0.4.4 (2012-05-01)
^^^^^^^^^^^^^^^^^^

* not distribute util3.py (alternative print for python3)

0.4.3 (2012-05-01)
^^^^^^^^^^^^^^^^^^

* search target conent and type
* retrieve all zone

0.4.2 (2012-04-28)
^^^^^^^^^^^^^^^^^^

* Add search records
* Format of stdout of retrieve records

0.4.1 (2012-04-27)
^^^^^^^^^^^^^^^^^^

* Fix bug processing last data only, when separate file

0.4 (2012-04-26)
^^^^^^^^^^^^^^^^

* default option config file $HOME/.tdclirc


0.3.2 (2012-04-25)
^^^^^^^^^^^^^^^^^^

* Add unittest of pep8, converter.py, tdauth.py (partially) 
* Add exception error handling
* Refactoring (Thanks Henrich)


0.3.1 (2012-04-23)
^^^^^^^^^^^^^^^^^^

* Add manpage


0.3 (2012-04-21)
^^^^^^^^^^^^^^^^

* New command line style, add sub-command, change options

  * Change optparse to argparse
  * new sub-command : show|get|create|delete


0.2 (2012-04-20)
^^^^^^^^^^^^^^^^

* Support Python3
* Add option `-P` as password prompt with echo turned off

0.1 (2012-04-20)
^^^^^^^^^^^^^^^^

* first release

