# tiny-json-log

Compact and easy to use json logging lib

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

## Formatting 

You can also pass a format string to control what [logRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes) are printed. Format string is a space separate list of logRecord attrs enclosed in `{}`. For example 


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

By default key names of a log are equal logRecord attribute names. You can change this behaviour by specifing `<custom attr key>={<some logRecord attr>}` for example

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
