JSON converter for TonicDNS
===========================

This converts from readble text record to JSON for TonicDNS; RESTful API for PowerDNS.

example.org.txt
---------------

.. code-block::

   # name type content ttl priority
   test0.example.org A 10.10.10.10 86400
   test1.example.org A 10.10.10.11 86400
   test2.example.org A 10.10.10.12 86400
   example.org MX mx.example.org 86400 0
   example.org MX mx2.example.org 86400 10
   mx.example.org A 10.10.11.10 3600
   mx2.example.org A               10.10.11.10 3600

Usage
-----

.. code-block:: shell

   $ python json-convert.py sample/example.org.txt
   {"records": [{"content": "10.10.10.10", "priority": null, "type": "A", "name": "test0.example.org", "ttl": "86400"}, {"content": "10.10.10.11", "priority": null, "type": "A", "name": "test1.example.org", "ttl": "86400"}, {"content": "10.10.10.12", "priority": null, "type": "A", "name": "test2.example.org", "ttl": "86400"}, {"content": "mx.example.org", "priority": "0", "type": "MX", "name": "example.org", "ttl": "86400"}, {"content": "mx2.example.org", "priority": "10", "type": "MX", "name": "example.org", "ttl": "86400"}, {"content": "10.10.11.10", "priority": null, "type": "A", "name": "mx.example.org", "ttl": "3600"}, {"content": "10.10.11.10", "priority": null, "type": "A", "name": "mx2.example.org", "ttl": "3600"}], "name": "example.org"}






