====================================
tonicdnscli is TonicDNS Client tool.
====================================

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

   
Usage
-----

Input file (example.org.txt)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

examples/example.org.txt::

   # name type content ttl priority
   test0.example.org A 10.10.10.10 86400
   test1.example.org A 10.10.10.11 86400
   test2.example.org A 10.10.10.12 86400
   example.org MX mx.example.org 86400 0
   example.org MX mx2.example.org 86400 10
   mx.example.org A 10.10.11.10 3600
   mx2.example.org A               10.10.11.10 3600


Setting default options to config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An alternative method of command options that use the config file.
Copy examples/tdclirc.sample to `$HOME/.tdclirc`. `password` key to set password in plain text, it is recommended that you remove this line, `-P` option is used.::

   [global]
   server: ns.example.org

   [auth]
   username: tonicuser
   password: tonicpw


Print converted JSON
^^^^^^^^^^^^^^^^^^^^

Convert to JSON and print.::

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

Retrieve all zones
^^^^^^^^^^^^^^^^^^

Get all zones and print.::

   $ tonicdnscli get -u tonicusername -P
   +-------------+--------+-----------------+
   | name        | type   | notified_serial |
   +-------------+--------+-----------------+
   | example.org | MASTER | 2012052201      |
   | example.net | MASTER | 2012060502      |
   +-------------+--------+-----------------+


Retrieve records
^^^^^^^^^^^^^^^^

Get records of specific zone and print.::

   $ tonicdnscli get -s ns.example.org -d example.org -u tonicusername -P
   zone:        example.org
   SOA record:  ns.example.org hostmaster.example.org 2012042403
   ttl:         86400 
   change date: 1341314161
   example.org
   +------+------+-----------------+-------+------+-------------+
   | name | type | content         | ttl   | prio | change date |
   +------+------+-----------------+-------+------+-------------+
   |      | NS   | ns.example.org  | 86400 | -    | -           |
   |      | NS   | ns2.example.org | 86400 | -    | -           |
   | ns.  | A    | 192.168.0.100   | 86400 | -    | -           |
   | ns2. | A    | 192.168.0.101   | 86400 | -    | -           |
   | www. | A    | 192.168.0.1     | 86400 | -    | -           |
   +------+------+-----------------+-------+------+-------------+


Create single record
^^^^^^^^^^^^^^^^^^^^

Create single record with specific zone.::

   $ tonicdnscli create -s ns.example.org -u tonicusername -P \
   --domain example.org --name www2.example.org --rtype A --content 10.10.10.10
   true

Create records
^^^^^^^^^^^^^^

Create multi records with specific zone.::

   $ tonicdnscli bulk_create -s ns.example.org -u tonicusername -P examples/example.org.txt
   true

Update single record
^^^^^^^^^^^^^^^^^^^^

Update single record with specific zone.::

  $ tonicdnscli update -s ns.example.org -u tonicdnsusername -P \
  --domain example.org --name www2.example.org --rtype A --content 10.10.10.10 --new-content 10.10.10.11
  true (<- delete record)
  true (<- create record)

Delete single records
^^^^^^^^^^^^^^^^^^^^^

Delete single record with specific zone.::

   $ tonicdnscli delete -s ns.example.org -u tonicusername -P \
   --domain example.org --name www2.example.org --rtype A --content 10.10.10.11
   true

Delete records
^^^^^^^^^^^^^^

Delete multi records with specific zone.::

   $ tonicdnscli bulk_delete -s ns.example.org -u tonicusername -P examples/example.org.txt
   true

Update SOA
^^^^^^^^^^

Update SOA record or speficie zone.::

   $ tonicdnscli soa -s ns.example.org -u tonicusername -P --domain example.org
   true (<- create record)
   true (<- delete record)

If you want to update automatically, append next variable to global section of ~/.tdclirc.::

  [global]
  (snip)
  soa_update: True


Create zone for MASTER
^^^^^^^^^^^^^^^^^^^^^^

Master DNS server IP address with `--dnsaddr` option.::

   $ tonicdnscli zone_create -s ns.example.org -u tonicusername -P --domain example.net --dnsaddr 192.168.0.100
   true
   true
   true


Create zone for SLAVE
^^^^^^^^^^^^^^^^^^^^^

Require `-S` option.::

   $ tonicdnscli zone_create -s ns.example.org -u tonicusername -P --domain example.net --dnsaddr 192.168.0.100 -S
   true (<- create template)
   true (<- create zone)
   true (<- delete template)

Create zone for NATIVE
^^^^^^^^^^^^^^^^^^^^^^

Require `-N` option.::

   $ tonicdnscli zone_create -s ns.example.org -u tonicusername -P --domain example.net --dnsaddr 192.168.0.100 -N
   true (<- create template)
   true (<- create zone)
   true (<- delete template)

Delete zone
^^^^^^^^^^^

Delete specific zone.::

   $ tonicdnscli zone_delete -s ns.example.org -u tonicusername -P --domain example.com
   true


Retrieve templates
^^^^^^^^^^^^^^^^^^

Get tepmlates and print.::

   $ tonicdnscli tmpl_get -s ns.example.org -u tonicusername -P
   identifier : example_net
   description: 
   ==============================================================================
   name                              type  content                   ttl   prio
   example.net                       SOA  
   > ns.example.net hostmaster.example.net 2012070501 3600 900 86400 3600   3600 
   example.net                       NS    ns.example.net            3600 
   ns.example.net                    A     192.168.0.100             3600 
   ==============================================================================
   identifier : example2_net
   description:
   (snip)


Delete template
^^^^^^^^^^^^^^^

Delete specific template.::

   $ tonicdnscli tmpl_delete -s ns.example.org -u tonicusername -P --template example_com
   true


Contribute
----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python2.7 later, and py.test. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-pytest

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.


See also
--------

* `TonicDNS <https://github.com/Cysource/TonicDNS>`_
* `PowerDNS <http://www.powerdns.com>`_

