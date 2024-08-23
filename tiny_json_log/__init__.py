import json
import logging
import typing as tp
import contextlib
import re


class JsonStyle(logging.StrFormatStyle):
    """
    JsonStyle is used to format log records to json
    JsonStyle can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes. Currently, the useful
    attributes in a LogRecord are described by:

     name              Name of the logger (logging channel)
     levelno           Numeric logging level for the message (DEBUG, INFO,
                       WARNING, ERROR, CRITICAL)
     levelname         Text logging level for the message ("DEBUG", "INFO",
                       "WARNING", "ERROR", "CRITICAL")
     pathname          Full pathname of the source file where the logging
                       call was issued (if available)
     filename          Filename portion of pathname
     module            Module (name portion of filename)
     lineno            Source line number where the logging call was issued
                       (if available)
     funcName          Function name
     created           Time when the LogRecord was created (time.time()
                       return value)
     asctime           Textual time when the LogRecord was created
     msecs             Millisecond portion of the creation time
     relativeCreated   Time in milliseconds when the LogRecord was created,
                       relative to the time the logging module was loaded
                       (typically at application startup time)
     thread            Thread ID (if available)
     threadName        Thread name (if available)
     process           Process ID (if available)
     message           The result of record.getMessage(), computed just as
                       the record is emitted

     Attributes should be wrapped in {} and be separated by space.
     By default attribute names (eg levelno, name, message etc)
     represent json key names. You can also specify custom key names
     like so 'key_name={attribute}'.
     Examples:
       '{message} {name} {process}'
       '{asctime}'
       'severity={levelname} logger={name} {message}'

    """

    default_format = "severity={levelname} logger={name} {message}"
    validation_pattern = re.compile(r"^((\w+=)*\{\w+\})( (\w+=)*\{\w+\})*$")

    def __init__(
        self,
        merge_message: bool,
        fmt: str,
        defaults: tp.Dict[str, tp.Any] | None = None,
    ) -> None:
        self._merge_message = merge_message
        super().__init__(fmt, defaults=defaults)

    def _format(self, record: logging.LogRecord) -> str:
        if defaults := self._defaults:
            values = defaults | record.__dict__
        else:
            values = record.__dict__

        format_dict = {}
        for key_and_attr in self._fmt.split(" "):
            splitted = key_and_attr.split("=")

            attr = splitted[-1].strip("{}")
            key = splitted[0].strip("{}")

            if (
                attr == "message"
                and self._merge_message
                and isinstance(values[attr], dict)
            ):
                format_dict = format_dict | values[attr]
            else:
                format_dict[key] = values[attr]

        return json.dumps(format_dict)

    def validate(self) -> None:
        """Validate the input format, ensure it is the correct string formatting style"""
        if not self.validation_pattern.search(self._fmt):
            raise ValueError(
                """Invalid format '{}'.
                Shoud be single space separated attributes wrapped in {{}}
                or 'customkey={{attribute}}'
                """.format(
                    self._fmt
                )
            )


class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        validate: bool = True,
        merge_message: bool = False,
        defaults: tp.Dict[str, tp.Any] | None = None,
    ) -> None:
        self._style = JsonStyle(merge_message, fmt, defaults)

        if validate:
            self._style.validate()

        self._fmt = self._style._fmt
        self.datefmt = datefmt

    def formatMessage(self, record: logging.LogRecord) -> str:
        # if message is in json format
        # convert to dict. If not
        # pass it as string
        with contextlib.suppress(json.decoder.JSONDecodeError):
            record.message = json.loads(record.message)

        return super().formatMessage(record)
