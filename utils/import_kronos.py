import argparse

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="Name of default project", default="Default")
    parser.add_argument(
        "--output-url",
        "-o",
        help="Base URL for hydra API",
        default="http://localhost:8000",
    )
    parser.add_argument(
        "--input-url",
        "-i",
        help="Base URL for kronos API",
        default="https://kronos.in.anthonyoteri.com",
    )
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)

    args = parser.parse_args()

    resp = requests.post(
        args.output_url + "/v1/auth/login/",
        json={"username": args.username, "password": args.password},
    )
    resp.raise_for_status()
    token = resp.json()["auth_token"]

    session = requests.Session()
    session.headers = {"authorization": f"Token {token}"}

    # Populate the project id_map
    id_map = {}
    resp = session.get(args.output_url + "/v1/categories/")
    resp.raise_for_status()
    for project in resp.json():
        id_map[project["name"]] = project["id"]

    # Fetch list of projects from Kronos
    resp = requests.get(args.input_url + "/api/projects")
    resp.raise_for_status()
    projects = resp.json()

    for project in projects:
        category_name = project["slug"]

        if category_name in id_map:
            continue

        body = {
            "name": category_name,
            "description": project["description"],
        }
        resp = session.post(args.output_url + "/v1/categories/", json=body)

        if resp.status_code == 201:
            resp = session.post(
                args.output_url + "/v1/projects/",
                json={
                    "name": args.project,
                    "description": "Created by import script",
                    "category": resp.json()["id"],
                },
            )

            if resp.status_code == 201:
                id_map[category_name] = resp.json()["id"]

    # Clean out existing records
    resp = session.get(args.output_url + "/v1/records/")
    resp.raise_for_status()
    for record in resp.json():
        session.delete(args.output_url + f"/v1/records/{record['id']}")

    # Insert new records from Kronos
    resp = requests.get(args.input_url + "/api/records")
    resp.raise_for_status()
    for record in reversed(resp.json()):
        body = {
            "project": id_map[record["project"]],
            "start_time": record["startTime"],
            "stop_time": record["stopTime"],
        }

        if record["startTime"] is None or record["stopTime"] is None:
            continue

        session.post(args.output_url + "/v1/records/", json=body).raise_for_status()


if __name__ == "__main__":
    main()
