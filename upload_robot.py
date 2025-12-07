import argparse
import requests

def upload(api_url, api_key, project_id, xml_file):
    files = {"junit_file": open(xml_file, "rb")}
    data = {
        "project_id": project_id,
        "name": "robot-ci",
        "environment": "staging",
        "triggered_by": "CI"
    }

    resp = requests.post(
        f"{api_url}/test-runs/robot",
        headers={"X-API-KEY": api_key},
        data=data,
        files=files
    )

    print(resp.status_code, resp.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--file", required=True)

    args = parser.parse_args()
    upload(args.api, args.key, args.project, args.file)
