import pytest
import datetime
from html_report_generator.report_generator import HTMLReports, LogStatus  # Assuming within your project structure



@pytest.fixture(scope="session", autouse=True)
def html_report():
    # Setup: initialize ExtentReports object
    global report
    report = HTMLReports(file_path="reports/test_report.html")
    yield report
    # Teardown: flush and generate report after all tests
    report.flush()
    print("Extent report generated.")


@pytest.fixture(scope="function", autouse=True)
def create_test(html_report, request):
    # Fixture that creates a new test instance per pytest test function
    test_name = request.node.name

    #module = request.module.__name__
    description = f"Test generated for {test_name}"

    test_instance = html_report.create_test(test_name, description)

    yield test_instance

    # Example: finalize test with pass or fail
    # This can be expanded to log more details based on the actual pytest outcome
    if request.node.rep_call.passed:
        test_instance.set_status(LogStatus.PASS)
    elif request.node.rep_call.failed:
        test_instance.set_status(LogStatus.FAIL)
    else:
        test_instance.set_status(LogStatus.SKIP)


import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if "create_test" in item.fixturenames:
        setattr(item, "rep_" + rep.when, rep)
