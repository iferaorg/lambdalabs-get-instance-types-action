import os
import requests


def main():
    available_only = os.getenv("AVAILABLE_ONLY", "true").lower() == "true"
    names_only = os.getenv("NAMES_ONLY", "false").lower() == "true"
    lambda_token = os.getenv("LAMBDA_TOKEN")

    if not lambda_token:
        raise ValueError("LAMBDA_TOKEN environment variable is not set")

    url = "https://cloud.lambdalabs.com/api/v1/instance-types"
    headers = {"Authorization": f"Bearer {lambda_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        error = response.json().get("error", {"message": "An unknown error occurred"})
        print(
            f'Error: {error["message"]}. Suggestion: {error.get("suggestion", "No suggestion available")}'
        )
        exit(1)

    instance_types = response.json().get("data", {})

    if available_only:
        instance_types = {
            k: v
            for k, v in instance_types.items()
            if v.get("regions_with_capacity_available")
        }

    if names_only:
        instance_type_names = list(instance_types.keys())
        print(f'::set-output name=instance_types::{",".join(instance_type_names)}')
    else:
        print(f"::set-output name=instance_types::{instance_types}")


if __name__ == "__main__":
    main()