# tiny-json-log

Compact and easy to use json logging lib

## Installing

**Pip**

```
pip install tiny-json-log
```

**Pypi**

https://pypi.org/project/tiny-json-log/



## Usage

To write logs in json simply pass an instance of `JSONFormatter` class to your handler


```
import logging
from tiny_json_log import JSONFormatter

#You can use any other handler 
#for example FileHandler
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

#Here we use root logger but
#you can use any logger you wish
root = logging.getLogger()
root.addHandler(handler)
root.setLevel("INFO")

root.info("informative message")
```

this will print to stderr

```
{"severity": "INFO", "logger": "root", "message": "informative message"}

```

## Json message

If your message string is in json format, library will convert it to json and nest it under `message` key

```
import logging
import json
import uuid
from tiny_json_log import JSONFormatter

log_dict = {
    "src": "module.some_class",
    "userid": f"{uuid.uuid4()}",
    "nested": {
        "some_nested_attr": 123
    }
}

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
root = logging.getLogger()
root.addHandler(handler)
root.setLevel("DEBUG")

root.info(json.dumps(log_dict))
```

this will print to stderr something like

```
{"severity": "INFO", "logger": "root", "message": {"src": "module.some_class", "userid": "32b8bf63-3958-4caa-b566-a500c898e429", "nested": {"some_nested_attr": 123}}}
```

you can also pass `merge_message=True` to `JSONFormatter` constructor and it will merge you JSON message with other logRecord attributes

```
import logging
import json
import uuid
from tiny_json_log import JSONFormatter

log_dict = {
    "src": "module.some_class",
    "userid": f"{uuid.uuid4()}",
    "nested": {
        "some_nested_attr": 123
    }
}

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter(merge_message=True))
root = logging.getLogger()
root.addHandler(handler)
root.setLevel("DEBUG")

root.info(json.dumps(log_dict))
```

will print

```
{"severity": "INFO", "logger": "root", "src": "module.some_class", "userid": "f10a8b6a-86c1-4280-8685-421ceea58811", "nested": {"some_nested_attr": 123}}
```

## Formatting 

You can also pass a format string to control what [logRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes) are printed. Format string is a space separated list of logRecord attrs enclosed in `{}`. For example 


```
import logging
from tiny_json_log import JSONFormatter


fmt = "{levelname} {message} {name}" 

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter(fmt))

root = logging.getLogger()
root.addHandler(handler)
root.setLevel("DEBUG")

root.error("informative message")
```

this will print to stderr

```
{"levelname": "ERROR", "message": "informative message", "name": "root"}
```

By default log key names are equal to logRecord attribute names. You can change this behaviour by specifing `<custom attr key>={<some logRecord attr>}` for example

```
import logging
import sys
from tiny_json_log import JSONFormatter


fmt = "lvl={levelname} {message} logger={name}"

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter(fmt))

root = logging.getLogger()
root.addHandler(handler)
root.setLevel("DEBUG")

root.info("informative message")
```

this will print to stdout

```
{"lvl": "INFO", "message": "informative message", "logger": "root"}
```

**Default format string is** `severity={levelname} logger={name} {message}`
