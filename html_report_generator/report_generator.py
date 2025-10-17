import json
import datetime
import os
import importlib


from .report_entities import LogStatus, Html_Test

class HTMLReports:
    DEFAULT_DASHBOARD_PATH = os.path.join(os.path.dirname(__file__), "html_files", "dashboard.html")
    DEFAULT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "html_files", "report_template.html")
    DEFAULT_MAIN_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "html_files", "main_template.html")

    def __init__(self, file_path,
                 dashboard_path=None,
                 template_path=None,
                 main_template_path=None,
                 environment=None):
        self.file_path = file_path
        self.dashboard_path = dashboard_path or HTMLReports.DEFAULT_DASHBOARD_PATH
        self.template_path = template_path or HTMLReports.DEFAULT_TEMPLATE_PATH
        self.main_template_path = main_template_path or HTMLReports.DEFAULT_MAIN_TEMPLATE_PATH

        self.tests = []
        self.environment = environment if environment else {
            "browser": "chrome",
            "environment": "staging",
            "thread": "1",
            "report_name": "Automation report"
        }

    def create_test(self, name, module, description="", annotations=None, test_id=None, markers=None):
        tags = [module]
        if annotations:
            tags.extend(annotations)
        if markers:
            tags.extend(str(m) for m in markers)
        tags = list(dict.fromkeys(tags))
        test = Html_Test(name, module, description, tags, test_id)
        self.tests.append(test)
        return test

    def flush(self):
        for test in self.tests:
            test.end()
        pass_cnt = sum(1 for t in self.tests if t.status == LogStatus.PASS)
        fail_cnt = sum(1 for t in self.tests if t.status == LogStatus.FAIL)
        skip_cnt = sum(1 for t in self.tests if t.status == LogStatus.SKIP)
        pass_percent = int(100 * pass_cnt / max(1, pass_cnt + fail_cnt + skip_cnt))

        start_times = [datetime.datetime.strptime(t.start_time, "%m.%d.%Y %I:%M:%S %p") for t in self.tests]
        end_times = [datetime.datetime.strptime(t.end_time, "%m.%d.%Y %I:%M:%S %p") for t in self.tests]
        overall_start = min(start_times).strftime("%b %d, %Y %I:%M:%S %p") if start_times else "-"
        overall_end = max(end_times).strftime("%b %d, %Y %I:%M:%S %p") if end_times else "-"
        overall_duration = str(max(end_times) - min(start_times)) if (start_times and end_times) else "-"

        env_html_rows = ""
        for key, value in self.environment.items():
            env_html_rows += f"<tr><td style='padding:6px; border-bottom:1px solid #ccc;'>{key.capitalize()}</td>" \
                             f"<td style='padding:6px; border-bottom:1px solid #ccc;'>{value}</td></tr>"

        module_stats = {}
        for t in self.tests:
            mod = t.module
            if mod not in module_stats:
                module_stats[mod] = {"passed": 0, "failed": 0, "skip": 0, "others": 0}
            if t.status == LogStatus.PASS:
                module_stats[mod]["passed"] += 1
            elif t.status == LogStatus.FAIL:
                module_stats[mod]["failed"] += 1
            elif t.status == LogStatus.SKIP:
                module_stats[mod]["skip"] += 1
            else:
                module_stats[mod]["others"] += 1

        tags_rows = ""
        for mod, stats in module_stats.items():
            total = stats["passed"] + stats["failed"] + stats["skip"] + stats["others"]
            pass_percent_module = f"{(stats['passed']/total*100):.1f}" if total > 0 else "0"
            tags_rows += f"""
            <tr>
                <td style="padding:8px; border:1px solid #ccc;">{mod}</td>
                <td style="padding:8px; border:1px solid #ccc; text-align:center;">{stats['passed']}</td>
                <td style="padding:8px; border:1px solid #ccc; text-align:center;">{stats['failed']}</td>
                <td style="padding:8px; border:1px solid #ccc; text-align:center;">{stats['skip']}</td>
                <td style="padding:8px; border:1px solid #ccc; text-align:center;">{stats['others']}</td>
                <td style="padding:8px; border:1px solid #ccc; text-align:center;">{pass_percent_module}%</td>
            </tr>
            """

        with open(self.dashboard_path, "r", encoding="utf-8") as df:
            dashboard_html = df.read().format(
                overall_start=overall_start,
                overall_end=overall_end,
                duration=overall_duration,
                pass_cnt=pass_cnt,
                fail_cnt=fail_cnt,
                skip_cnt=skip_cnt,
                pass_percent=pass_percent,
                browser=self.environment["browser"],
                environment=self.environment["environment"],
                environment_html=env_html_rows,
                thread=self.environment["thread"],
                tags_html=tags_rows
            )

        # After generating dashboard_html as shown previously

        # Group tests by modules for report details
        module_map = {}
        for test in self.tests:
            #module_map.setdefault(test.module, []).append(test)
            try:
                mod_obj = importlib.import_module(test.module)
                module_name_override = getattr(mod_obj, "module_name", None)
            except ImportError:
                module_name_override = None

            mod_key = module_name_override if module_name_override else test.module

            module_map.setdefault(mod_key, []).append(test)

        # Prepare module entries HTML & JSON data
        module_entries = '''
        <script>
        document.addEventListener("DOMContentLoaded", function() {
          const search = document.getElementById("moduleSearch");
          search.addEventListener("keyup", function() {
            let filter = search.value.toLowerCase();
            let modules = document.querySelectorAll(".module");
            let lists = document.querySelectorAll(".test-list");
            for(let i=0; i<modules.length; i++) {
              let txt = modules[i].textContent.trim().toLowerCase();
              if(txt.includes(filter)) {
                modules[i].style.display = "";
                lists[i].style.display = "";
              } else {
                modules[i].style.display = "none";
                lists[i].style.display = "none";
              }
            }
          });
        });
        </script>
        '''
        module_json = []

        for mod_idx, (mod, testlist) in enumerate(module_map.items()):
            module_entries += f"""
        <div class='module' onclick='toggleModule({mod_idx})' id='modbtn{mod_idx}'>
          <span>{mod}</span>
          <svg width='17' height='17' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg' 
              style='margin-left:10px;vertical-align:middle;'>
            <path d='M5 8l5 5 5-5' stroke='#7e5fcf' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/>
          </svg>
        </div>
        """

            def get_status_class(status):
                status = status.lower()
                if status == "pass":
                    return "status-badge pass"
                if status == "fail":
                    return "status-badge fail"
                if status == "skip":
                    return "status-badge skip"
                return "status-badge"

            module_entries += f"<div class='test-list' id='testlist{mod_idx}'>"
            for test_idx, test in enumerate(testlist):
                status_class = get_status_class(test.status.value)
                module_entries += (
                    f"<div class='test-row'>"
                    f"<div class='test-btn-text' id='testbtn_{mod_idx}_{test_idx}' "
                    f"onclick='showTest({mod_idx},{test_idx});event.stopPropagation();'>"
                    f"{test.name}"
                    f"<span class='{status_class}'>{test.status.value}</span>"
                    f"</div>"
                    f"<hr class='test-separator' />"
                    f"</div>")
            module_entries += "</div>"

            module_json.append({
                'module': mod,
                'tests': [
                    {
                        'name': t.name,
                        'description': t.description,
                        'annotations': t.annotations,
                        'status': t.status.value,
                        'steps': [{
                            'status': s.status.value,
                            'message': s.message,
                            'timestamp': s.timestamp,
                            'screenshot': s.screenshot
                        } for s in t.steps],
                        'start_time': t.start_time,
                        'duration': t.duration,
                        'test_id': t.test_id
                    } for t in testlist
                ]
            })

        # Read and fill report template
        with open(self.template_path, "r", encoding="utf-8") as tf:
            report_html = tf.read().format(
                module_entries=module_entries,
                test_data_json=json.dumps(module_json)
            )

        # Read main template and compose final file
        with open(self.main_template_path, "r", encoding="utf-8") as mf:
            main_template = mf.read()

        with open(self.file_path, "w", encoding="utf-8") as outf:
            outf.write(main_template.format(
                dashboard_html=dashboard_html,
                report_html=report_html,
                report_name=self.environment.get("report_name", "Automation Report")
            ))

        print(f"Report generated: {self.file_path}")



