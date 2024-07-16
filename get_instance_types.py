"""Module to fetch and display Lambda Labs cloud instance types."""

import json
import os
import sys

import requests


def main():
    """Fetch and display Lambda Labs cloud instance types from environment settings."""
    available_only = os.getenv("AVAILABLE_ONLY", "true").lower() == "true"
    names_only = os.getenv("NAMES_ONLY", "false").lower() == "true"
    lambda_token = os.getenv("LAMBDA_TOKEN")

    if not lambda_token:
        raise ValueError("LAMBDA_TOKEN environment variable is not set")

    url = "https://cloud.lambdalabs.com/api/v1/instance-types"
    headers = {"Authorization": f"Bearer {lambda_token}"}

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        error = response.json().get("error", {"message": "An unknown error occurred"})
        print(
            f'Error: {error["message"]}. '
            f'Suggestion: {error.get("suggestion", "No suggestion available")}'
        )
        sys.exit(1)

    instance_types = response.json().get("data", {})

    if available_only:
        instance_types = {
            k: v
            for k, v in instance_types.items()
            if v.get("regions_with_capacity_available")
        }

    if names_only:
        instance_type_names = list(instance_types.keys())
        output_str = ",".join(instance_type_names)
    else:
        output_str = json.JSONEncoder().encode(instance_types)

    # Get the path to the GITHUB_OUTPUT environment file
    output_file_path = os.getenv("GITHUB_OUTPUT")

    # Write the output to the GITHUB_OUTPUT environment file
    if output_file_path is not None:
        with open(output_file_path, "a", encoding="utf-8") as file:
            file.write(f"instance_types={output_str}\n")
    else:
        raise ValueError("GITHUB_OUTPUT environment variable is not set.")


if __name__ == "__main__":
    main()
