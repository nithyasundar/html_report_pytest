"""
Entry point / orchestrator for HTML report generation.

This module provides ReportGenerator which ties together:
- data collection (data_collector)
- rendering (renderer)
- utilities (utils)

This is intentionally thin — all heavy logic is in the other modules.
"""
from typing import Any, Iterable
from .data_collector import collect_report_data
from .renderer import Renderer
from .utils import write_file_atomic


class ReportGenerator:
    """
    High-level API for generating HTML reports.
    Usage:
        gen = ReportGenerator()
        html = gen.generate(report_items)
        gen.write(html, "report.html")
    """

    def __init__(self, title: str = "PyTest HTML Report"):
        self.title = title
        self.renderer = Renderer(title=title)

    def generate(self, report_items: Iterable[Any]) -> str:
        """
        Convert raw report items to HTML string.

        report_items: Iterable of pytest result objects or dict-like test results.
        """
        data = collect_report_data(report_items)
        return self.renderer.render(data)

    def write(self, html: str, path: str, *, encoding: str = "utf-8") -> None:
        """
        Atomically write the generated HTML to disk.
        """
        write_file_atomic(path, html.encode(encoding))