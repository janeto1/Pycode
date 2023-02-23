import pytest
from utils.logger import Log

log = Log().logger


class TestTester:

    def test_case1(self, ):
        log.error("*"*100)
        assert 1 == 2


if __name__ == '__main__':
    pytest.main(["-s", "test_pytest.py"])
