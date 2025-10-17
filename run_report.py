from html_report_generator.report_generator import HTMLReports
from html_report_generator.report_entities import LogStatus

if __name__ == "__main__":
    report = HTMLReports(
        file_path="./reports/report.html"
    )
    t1 = report.create_test(
        name="Verify Fact Layout",
        module="ConversationDetailsSanity",
        description="verify the Fact explanation should be from left to right in English",
        annotations=["Sanity", "UI"],
        test_id="test-id=6"
    )
    t1.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t1.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t1.log(LogStatus.PASS, "Refresh the page")
    t2 = report.create_test(
        name="Verify login",
        module="Bulk",
        description="verify the Bulk explanation should be from left to right in English",
        annotations=["XXXX", "UI"],
        test_id="test-id=1"
    )
    t2.log(LogStatus.FAIL, "Delete cookies and clear local/session storage.")
    t2.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t2.log(LogStatus.PASS, "Refresh the page")
    t3 = report.create_test(
        name="Verify login Layout",
        module="ConversationDetailsSanity",
        description="verify the login in English",
        annotations=["Sanity", "UI"],
        test_id="test-id=6"
    )
    t3.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t3.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t3.log(LogStatus.PASS, "Refresh the page")

    t4 = report.create_test(
        name="Verify Fact Layout",
        module="LLM",
        description="verify the Fact explanation should be from left to right in English",
        annotations=["Sanity", "UI"],
        test_id="test-id=6"
    )
    t4.log(LogStatus.SKIP, "Delete cookies and clear local/session storage.")
    t4.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t4.log(LogStatus.PASS, "Refresh the page")
    t5 = report.create_test(
        name="Verify logout",
        module="Bulk",
        description="verify the logout to right in English",
        annotations=["Sanity", "UI"],
        test_id="test-id=6"
    )
    t5.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t5.log(LogStatus.PASS, "Delete cookies and clear local/session storage.")
    t5.log(LogStatus.PASS, "Refresh the page")
    report.flush()
