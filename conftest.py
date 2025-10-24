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

def get_module_name_pytest_module(module):
    # Fetch module_name if defined, fallback to module.__name__
    return getattr(module, "module_name", module.__name__)


@pytest.fixture(scope="function", autouse=True)
def create_test(html_report, request):
    test_name = request.node.name
    description = f"Test generated for {test_name}"

    # Get module_name attribute from the test module if defined
    module = request.module
    module_val = get_module_name_pytest_module(module)

    # If module_name is a list, join with commas or handle how you like
    if isinstance(module_val, list):
        module_val = ", ".join(module_val)

    test_instance = html_report.create_test(
        name=test_name,
        module=module_val,
        description=description
    )

    yield test_instance

    if hasattr(request.node, "rep_call"):
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
