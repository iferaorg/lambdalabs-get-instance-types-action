# Get LambdaLabs Instance Types Action

This GitHub Action retrieves the instance types offered by Lambda GPU Cloud and optionally filters based on availability.

## Inputs

### `available_only`

**Required**: No  
**Default**: `true`  
**Description**: Filter out instance types with no available regions.

### `names_only`

**Required**: No  
**Default**: `false`  
**Description**: Return only the names of the instance types.

## Outputs

### `instance_types`

**Description**: The filtered list of instance types or instance type names.

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
      uses: actions/checkout@v2

    - name: Get Instance Types
      uses: ./
      with:
        available_only: ${{ inputs.available_only }}
        names_only: ${{ inputs.names_only }}
      env:
        LAMBDA_TOKEN: ${{ secrets.LAMBDA_TOKEN }}
    
    - name: Print Instance Types
      run: echo ${{ steps.get-instance-types.outputs.instance_types }}
