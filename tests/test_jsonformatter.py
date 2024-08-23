import logging
import pytest
import json
import uuid
from tiny_json_log import JSONFormatter

LOG_DICT = {
    "src": "module.some_class",
    "userid": str(uuid.uuid4()),
    "nested": {"some_nested_attr": 123},
}


class CustomHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_record = None

    def emit(self, record):
        self.log_record = self.format(record)


class TestJSONFormatter:
    def test_non_json_message(self):
        logging.info("test")
        record = json.loads(test_handler.log_record)
        assert "test" == record["message"]

    def test_json_message(self):
        logging.info(json.dumps(LOG_DICT))
        record = json.loads(test_handler.log_record)
        assert 123 == record["message"]["nested"]["some_nested_attr"]

    def test_json_message_merge(self):
        test_logger = logging.getLogger("test_logger")
        test_handler_message_merge = CustomHandler()
        test_handler_message_merge.setFormatter(JSONFormatter(merge_message=True))
        test_logger.addHandler(test_handler_message_merge)

        test_logger.info(json.dumps(LOG_DICT))
        record = json.loads(test_handler_message_merge.log_record)
        assert 123 == record["nested"]["some_nested_attr"]

    @pytest.mark.parametrize(
        "fmt, record_key, record_value",
        [
            # 20 is int representation of INFO level
            ("{levelno}", "levelno", 20),
            ("test={levelno}", "test", 20),
            ("test={levelno} {levelname}", "levelname", "INFO"),
            ("{levelno} logger={name} lvl={levelname}", "logger", "test_logger"),
        ],
    )
    def test_custom_format(self, fmt, record_key, record_value):
        test_logger = logging.getLogger("test_logger")
        test_handler_custom_fmt = CustomHandler()
        test_handler_custom_fmt.setFormatter(JSONFormatter(fmt))
        test_logger.addHandler(test_handler_custom_fmt)

        test_logger.info("test")

        record = json.loads(test_handler_custom_fmt.log_record)

        assert record_value == record[record_key]

    @pytest.mark.parametrize(
        "invalid_fmt",
        [
            # two spaces
            "{name}  {message}",
            # no {}
            "name  message",
            # partial {}
            "name  {message}",
            # special chars
            "!@#$%^&*()-=+]{<>?/'",
        ],
    )
    def test_validation_error(self, invalid_fmt):
        with pytest.raises(ValueError) as e:
            f = JSONFormatter(invalid_fmt)


test_handler = CustomHandler()
test_handler.setFormatter(JSONFormatter())
root = logging.getLogger()
root.addHandler(test_handler)
root.setLevel("DEBUG")
