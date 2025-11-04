"""
Render report data (from data_collector.collect_report_data) into an HTML string.
This renderer is simple and dependency-free (no Jinja2), using str.format for templating.
"""
from typing import Dict
from .templates import HTML_TEMPLATE
from .assets import DEFAULT_CSS
from .utils import format_duration, escape_html


class Renderer:
    def __init__(self, title: str = "PyTest HTML Report"):
        self.title = title
        self.css = DEFAULT_CSS

    def render(self, data: Dict) -> str:
        """
        Renders the report data into a complete HTML document.
        """
        counts = data.get("counts", {})
        duration_total = data.get("duration_total", 0.0)
        tests = data.get("tests", [])

        tests_html = []
        for t in tests:
            tests_html.append(
                "<tr class='test {outcome}'>"
                "<td class='nodeid'>{nodeid}</td>"
                "<td class='outcome'>{outcome}</td>"
                "<td class='duration'>{duration}</td>"
                "<td class='details'>{details}</td>"
                "</tr>".format(
                    nodeid=escape_html(t.get("nodeid", "")),
                    outcome=escape_html(t.get("outcome", "")),
                    duration=format_duration(t.get("duration", 0.0)),
                    details=escape_html(str(t.get("longrepr", ""))),
                )
            )

        html = HTML_TEMPLATE.format(
            title=escape_html(self.title),
            css=self.css,
            generated_at=format_duration(data.get("generated_at", 0.0), absolute=True),
            count_passed=counts.get("passed", 0),
            count_failed=counts.get("failed", 0),
            count_skipped=counts.get("skipped", 0),
            count_total=counts.get("total", 0),
            duration_total=format_duration(duration_total),
            tests_table="\n".join(tests_html),
        )
        return html