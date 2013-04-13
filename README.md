Negi
====

Negi(禰宜) is a command line tool for building static html file.
Negi combines Jinja2 template and JSON data, and builds html(or other format) files.


Requirements
------------
python2.7+

Dependencies
------------
* [Jinja2](http://jinja.pocoo.org/docs/)
* [aaaargh](https://github.com/wbolster/aaargh)


Install
-------

```
python setup.py install
```

Usage
-----
Setup directories like:

```
project_dir/
    data/   : JSON data directory
    dist/   : Output directory
    templates/      :Jinja2 Template directory
```

Then, on your project_dir, hit command:

```
negi build
```

You can change directories via command line options. See `negi build -h`.

Data(JSON) file structure
---------

```
data/
    __init__.json           : Loaded first. You can define global params of this directory and pages of this directory. 
    _paramname.json         : Used as global parameter named as "paramname"
    pagename.json           : Renderd as /pagename.html or definition for html files of /pagename/ directory (if has "_content" parameter in file)
    pagename_paramname.json : Used as parameter of /pagename.html
    _paramtext.txt          : You can use other format files. (simply used as text parameter)
    sub_dir/
        __init__.json       : Define global params for files under "sub_dir" directory and pages of this directory.
        index.json          : Renderd as /sub_dir/index.html with parameter of this file
```


JSON data structure
---------------

```
{
    "IMG_PATH":"/img",              // global "IMG_PATH" parameter
    "title":"site title",           // global "title" parameter
    "_contents":{                   // "_contents" is special param to define pages of this directory.
        "index":{                   // meaning create "index.html" to this directory.
            "title":"index"         // override global "title" parameter
        },
        "contact":{
            "title":"contact",
            "_ext":"cgi"            // set "_ext" param to change extension ("contact.html" -> "contact.cgi")
        }
    }
}
```
All parameter (except "_contents") automatically inherited from parent directory.


Rule of finding template
------------

Templates automatically assigned based on output file path. 



### Output path: /index.html

Search template directory:
```
/index.html
/__base__.html
```
and use template found first.


### Output path: /spam/egg/ham.php

Search template directory:
```
/spam/egg/ham.php
/spam/egg/ham.html
/spam_egg_ham.php
/spam_egg_ham.html
/spam/egg/__base__.php
/spam/egg/__base__.html
/spam/egg.php
/spam/egg.html
/spam_egg.php
/spam_egg.html
/spam/__base__.php
/spam/__base__.html
/spam.php
/spam.html
/__base__.php
/__base__.html
```
and use template found first
