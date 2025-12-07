from typing import List, Tuple, Optional
from lxml import etree


def parse_junit_xml(xml_bytes: bytes) -> Tuple[List[dict], dict]:
    """
    Parse JUnit XML menjadi list testcases + summary.

    Return:
        testcases: List[{
            "name": str,
            "classname": Optional[str],
            "status": "passed"/"failed"/"skipped"/"error",
            "duration": Optional[float],
            "message": Optional[str],
        }]
        summary: {
            "total": int,
            "passed": int,
            "failed": int,
            "skipped": int,
        }
    """
    root = etree.fromstring(xml_bytes)

    testcases = []
    total = passed = failed = skipped = 0

    # handle <testsuite> inside <testsuites> or directly
    if root.tag == "testsuites":
        suites = root.findall(".//testsuite")
    elif root.tag == "testsuite":
        suites = [root]
    else:
        suites = []

    for suite in suites:
        for tc in suite.findall("testcase"):
            total += 1
            name = tc.get("name") or "unnamed"
            classname = tc.get("classname")
            time_str = tc.get("time")
            duration = float(time_str) if time_str is not None else None

            status = "passed"
            message: Optional[str] = None

            failure = tc.find("failure")
            error = tc.find("error")
            skipped_el = tc.find("skipped")

            if failure is not None:
                status = "failed"
                message = (failure.get("message") or "") + "\n" + (failure.text or "")
                failed += 1
            elif error is not None:
                status = "error"
                message = (error.get("message") or "") + "\n" + (error.text or "")
                failed += 1
            elif skipped_el is not None:
                status = "skipped"
                message = (skipped_el.get("message") or "") + "\n" + (skipped_el.text or "")
                skipped += 1
            else:
                passed += 1

            testcases.append(
                {
                    "name": name,
                    "classname": classname,
                    "status": status,
                    "duration": duration,
                    "message": message.strip() if message else None,
                }
            )

    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
    }
    return testcases, summary
