# New file - report utility moved from conftest.py
import pytest
from html_report_generator.report_generator import HTMLReports, LogStatus


@pytest.fixture(scope="session", autouse=True)
def html_report():
    """
    Session-scoped fixture that creates the HTMLReports instance and
    flushes it at the end of the session.
    """
    report = HTMLReports(file_path="reports/test_report.html")
    try:
        yield report
    finally:
        report.flush()
        print("Extent report generated.")


def get_module_name_pytest_module(module):
    """
    Helper: fetch module_name if defined on the test module, otherwise fallback
    to module.__name__.
    """
    return getattr(module, "module_name", module.__name__)


@pytest.fixture(scope="function", autouse=True)
def create_test(html_report, request):
    """
    Function-scoped fixture that creates a test instance in the report before
    each test and updates its status after the test run (uses attributes set
    on the request.node by the pytest_runtest_makereport hook).
    """
    test_name = request.node.name
    description = f"Test generated for {test_name}"

    # Get module_name attribute from the test module if defined
    module = request.module
    module_val = get_module_name_pytest_module(module)

    # If module_name is a list, join with commas
    if isinstance(module_val, list):
        module_val = ", ".join(module_val)

    test_instance = html_report.create_test(
        name=test_name,
        module=module_val,
        description=description
    )

    yield test_instance

    # Update test status based on the report stored by the hook
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed:
            test_instance.set_status(LogStatus.PASS)
        elif request.node.rep_call.failed:
            test_instance.set_status(LogStatus.FAIL)
        else:
            test_instance.set_status(LogStatus.SKIP)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to save the per-stage test report on the item so fixtures can access
    the call result (e.g., request.node.rep_call).
    """
    outcome = yield
    rep = outcome.get_result()
    if "create_test" in item.fixturenames:
        setattr(item, "rep_" + rep.when, rep)