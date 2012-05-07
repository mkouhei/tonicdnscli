`tonicdnscli` is TonicDNS Client tool.
======================================

This command line tool for TonicDNS API.
TonicDNS is  RESTful API for PowerDNS.
Convert readble text record to JSON, and create or delete zone records with TonicDNS.


Requirements
------------

* Python 2.7 or Python 3.2 later.


Setup
-----
::

   $ git clone https://github.com/mkouhei/tonicdnscli
   $ cd tonicdnscli
   $ sudo python setup.py install

   
History
-------

0.5.1 (2012-05-07)
~~~~~~~~~~~~~~~~~~

* Fix bug get fail when resolver is SLAVE

0.5 (2012-05-04)
~~~~~~~~~~~~~~~~

* templates CRUD

0.4.4 (2012-05-01)
~~~~~~~~~~~~~~~~~~

* not distribute util3.py (alternative print for python3)

0.4.3 (2012-05-01)
~~~~~~~~~~~~~~~~~~

* search target conent and type
* retrieve all zone

0.4.2 (2012-04-28)
~~~~~~~~~~~~~~~~~~

* Add search records
* Format of stdout of retrieve records

0.4.1 (2012-04-27)
~~~~~~~~~~~~~~~~~~

* Fix bug processing last data only, when separate file

0.4 (2012-04-26)
~~~~~~~~~~~~~~~~

* default option config file $HOME/.tdclirc


0.3.2 (2012-04-25)
~~~~~~~~~~~~~~~~~~

* Add unittest of pep8, converter.py, tdauth.py (partially) 
* Add exception error handling
* Refactoring (Thanks Henrich)


0.3.1 (2012-04-23)
~~~~~~~~~~~~~~~~~~

* Add manpage


0.3 (2012-04-21)
~~~~~~~~~~~~~~~~

* New command line style, add sub-command, change options

  * Change optparse to argparse
  * new sub-command : show|get|create|delete


0.2 (2012-04-20)
~~~~~~~~~~~~~~~~

* Support Python3
* Add option `-P` as password prompt with echo turned off

0.1 (2012-04-20)
~~~~~~~~~~~~~~~~
* first release


Usage
-----

Input file (example.org.txt)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   # name type content ttl priority
   test0.example.org A 10.10.10.10 86400
   test1.example.org A 10.10.10.11 86400
   test2.example.org A 10.10.10.12 86400
   example.org MX mx.example.org 86400 0
   example.org MX mx2.example.org 86400 10
   mx.example.org A 10.10.11.10 3600
   mx2.example.org A               10.10.11.10 3600


Setting default options to config file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An alternative method of command options that use the config file.
Copy examples/tdclirc.sample to `$HOME/.tdclirc`. `password` key to set password in plain text, it is recommended that you remove this line, `-P` option is used.
::

   [global]
   server: ns.example.org

   [auth]
   username: tonicuser
   password: tonicpw



Print converted JSON
~~~~~~~~~~~~~~~~~~~~
::

   $ tonicdnscli show sample/example.org.txt
   {
     "records": [
       {
         "content": "10.10.10.10", 
         "name": "test0.example.org", 
         "ttl": "86400", 
         "type": "A"
       }, 
       {
         "content": "10.10.10.11", 
         "name": "test1.example.org", 
         "ttl": "86400", 
         "type": "A"
       }, 
       {
         "content": "10.10.10.12", 
         "name": "test2.example.org", 
         "ttl": "86400", 
         "type": "A"
       }, 
   (snip)


Retrieve records
~~~~~~~~~~~~~~~~
::

   $ tonicdnscli get -s ns.example.org -d example.org -u tonicusername -P
   domain: example.org
   serial: 2012042403
   DNS   : MASTER
   ==============================================================================
   name                              type  content                   ttl   prio
   ==============================================================================
   example.org                       SOA  
   >            ns.example.org hostmaster.example.org 2012042403  86400 
   example.org                       NS    ns.example.org            86400 
   example.org                       NS    ns2.example.org           86400 
   ns.example.org                    A     192.168.0.100             86400 
   ns2.example.org                   A     192.168.0.101             86400 
   www.example.org                   A     192.168.0.1               86400 
   ==============================================================================


Create records
~~~~~~~~~~~~~~
::

   $ tonicdnscli create -s ns.example.org -u tonicusername -P sample/example.org.txt
   True


Delete records
~~~~~~~~~~~~~~~
::

   $ tonicdnscli delete -s ns.example.org -u tonicusername -P sample/example.org.txt
   True


See also
--------

* `TonicDNS <https://github.com/Cysource/TonicDNS>`_
* `PowerDNS <http://www.powerdns.com>`_
