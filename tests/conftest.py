from dotenv import load_dotenv

from tests.cost_tracker import display_total_usage


def pytest_configure():
    load_dotenv()


def pytest_sessionfinish(session, exitstatus):
    display_total_usage()
