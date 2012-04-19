JSON converter for TonicDNS
===========================

This converts from readble text record to JSON for TonicDNS; RESTful API for PowerDNS.

example.org.txt
---------------

```
# name type content ttl priority
test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400
example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600
mx2.example.org A               10.10.11.10 3600
```

Install
-------

```bash
$ git clone https://github.com/mkouhei/tonicdns_cli
$ cd tonicdns_cli
$ sudo python setup.py install
```

Usage
-----

#### Print converted JSON

```bash
$ tonicdns_cli -o sample/example.org.txt
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
```

#### Retrieve records

```bash
$ tonicdns_cli -g -s ns.example.org -u tonicusername -p tonicpassword sample/example.org.txt
{
  "name": "example.org", 
  "notified_serial": "2012021402", 
  "records": [
    {
      "content": "ns.example.org hostmaster.example.org 2012021402", 
      "name": "example.org", 
      "priority": null, 
      "ttl": "86400", 
      "type": "SOA"
    }, 
    {
      "content": "ns.example.org", 
      "name": "example.org", 
      "priority": null, 
      "ttl": "86400", 
      "type": "NS"
    }, 
(snip)
```


#### Create records

```bash
$ tonicdns_cli -c -s ns.example.org -u tonicusername -p tonicpassword sample/example.org.txt
True
```

#### Delete records.

```bash
$ tonicdns_cli -d -s ns.example.org -u tonicusername -p tonicpassword sample/example.org.txt
True
```





