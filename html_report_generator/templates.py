# HTML template used by renderer.
# Placeholders used with str.format:
# title, css, generated_at, count_passed, count_failed, count_skipped,
# count_total, duration_total, tests_table
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <div class="summary">
      <span class="passed">Passed: {count_passed}</span>
      <span class="failed">Failed: {count_failed}</span>
      <span class="skipped">Skipped: {count_skipped}</span>
      <span class="total">Total: {count_total}</span>
      <span class="duration">Total time: {duration_total}</span>
      <span class="generated">Generated: {generated_at}</span>
    </div>
  </header>
  <main>
    <table class="tests">
      <thead>
        <tr><th>Test</th><th>Outcome</th><th>Duration</th><th>Details</th></tr>
      </thead>
      <tbody>
        {tests_table}
      </tbody>
    </table>
  </main>
</body>
</html>
"""