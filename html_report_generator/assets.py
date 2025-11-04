"""
Small place to keep CSS/JS assets as strings so templates stay clean.
"""
DEFAULT_CSS = """
body { font-family: Arial, sans-serif; font-size: 14px; color: #222; margin: 20px; }
header h1 { margin: 0 0 10px 0; }
.summary span { margin-right: 12px; padding: 4px 6px; border-radius: 4px; }
.passed { background: #e6ffed; color: #1b8f4a; }
.failed { background: #ffecec; color: #a33; }
.skipped { background: #fff7e6; color: #aa7a00; }
.tests { width: 100%; border-collapse: collapse; margin-top: 16px; }
.tests th, .tests td { text-align: left; padding: 6px; border-bottom: 1px solid #eee; }
.tests tr.failed { background: #fff6f6; }
.tests tr.passed { background: #f6fff6; }
.tests tr.skipped { background: #fffdf6; }
.nodeid { font-family: monospace; }
.details { white-space: pre-wrap; color: #444; font-size: 13px; }
"""