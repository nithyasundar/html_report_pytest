import datetime
import base64
import os
from enum import Enum
from typing import List

class LogStatus(Enum):
    PASS = "Pass"
    FAIL = "Fail"
    SKIP = "skip"
    INFO = "Info"

class TestStep:
    def __init__(self, status, message, screenshot_path=None, timestamp=None):
        self.status = status
        self.message = message
        self.timestamp = timestamp or datetime.datetime.now().strftime("%I:%M:%S %p")
        self.screenshot = ""
        if screenshot_path and os.path.isfile(screenshot_path):
            with open(screenshot_path, "rb") as imgf:
                img64 = base64.b64encode(imgf.read()).decode("utf-8")
                ext = screenshot_path.split('.')[-1].lower()
                mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
                self.screenshot = f"data:image/{mime};base64,{img64}"

class Html_Test:
    def __init__(self, name, module, description="", annotations=None, test_id=None, start_time=None):
        self.name = name
        self.module = module
        self.description = description
        self.annotations = annotations if annotations else []
        self.steps: List[TestStep] = []
        self.status = LogStatus.PASS
        self.test_id = test_id
        self.start_time = start_time or datetime.datetime.now().strftime("%m.%d.%Y %I:%M:%S %p")
        self.end_time = None
        self.duration = None

    def log(self, status, message, screenshot_path=None):
        step = TestStep(status, message, screenshot_path)
        self.steps.append(step)
        if status == LogStatus.FAIL:
            self.status = LogStatus.FAIL
        elif status == LogStatus.SKIP and self.status != LogStatus.FAIL:
            self.status = LogStatus.SKIP

    def end(self):
        self.end_time = datetime.datetime.now().strftime("%m.%d.%Y %I:%M:%S %p")
        try:
            start_dt = datetime.datetime.strptime(self.start_time, "%m.%d.%Y %I:%M:%S %p")
            end_dt = datetime.datetime.strptime(self.end_time, "%m.%d.%Y %I:%M:%S %p")
            self.duration = str(end_dt - start_dt)
        except Exception:
            self.duration = "-"

    def set_status(self, status):
        """
        Set the overall status of the test, upgrading only if status is worse.
        Priority order: FAIL > SKIP > PASS > INFO (or others)
        Uses LogStatus enums.
        """
        # Map LogStatus to severity rank
        severity = {
            LogStatus.FAIL: 3,
            LogStatus.SKIP: 2,
            LogStatus.PASS: 1,
            # Add others if needed, e.g., LogStatus.INFO: 0
        }

        # Normalize input to LogStatus if string is passed
        if isinstance(status, str):
            status = LogStatus[status.upper()]

        current_severity = severity.get(self.status, 0) if self.status else 0
        new_severity = severity.get(status, 0)

        if new_severity > current_severity:
            self.status = status
        elif self.status is None:
            self.status = status