import json
import argparse
import requests

def upload(api_url, api_key, project_id, json_file):
    payload = json.load(open(json_file))
    payload["project_id"] = int(project_id)

    resp = requests.post(
        f"{api_url}/load-runs/locust",
        headers={"X-API-KEY": api_key},
        json=payload
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
