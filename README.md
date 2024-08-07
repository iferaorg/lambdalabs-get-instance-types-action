# Get LambdaLabs Instance Types Action

[![MegaLinter](https://github.com/iferaorg/lambdalabs-get-instance-types-action/workflows/MegaLinter/badge.svg?branch=main)](https://github.com/iferaorg/lambdalabs-get-instance-types-action/actions?query=workflow%3AMegaLinter+branch%3Amain)

This GitHub Action retrieves the instance types offered by Lambda GPU Cloud and optionally filters based on availability.

## Inputs

### `available_only`

**Required**: No  
**Default**: `true`  
**Description**: Filter out instance types with no available regions.

### `names_only`

**Required**: No  
**Default**: `false`  
**Description**: Return only the names of the instance types. If false, return the full json payload from the LambdaLabs API.

### `lambda_token`

**Reqired**: Yes
**Description**: LambdaLabs API token

## Outputs

### `instance_types`

**Description**: The filtered list of instance types or instance type names. For the output schema documentation see <https://cloud.lambdalabs.com/api/v1/docs#operation/instanceTypes>.

## Example Usage

### Workflow Example

```yaml
name: Get LambdaLabs Instance Types

on:
  workflow_dispatch:
    inputs:
      available_only:
        description: 'Filter by availability'
        required: false
        default: 'true'
      names_only:
        description: 'Return names only'
        required: false
        default: 'false'

jobs:
  get-instance-types:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Get Instance Types
      uses: iferaorg/lambdalabs-get-instance-types-action@v1
      with:
        available_only: ${{ inputs.available_only }}
        names_only: ${{ inputs.names_only }}
        lamba_token: ${{ secrets.LAMBDA_TOKEN }}
    
    - name: Print Instance Types
      run: echo '${{ steps.get-instance-types.outputs.instance_types }}'
