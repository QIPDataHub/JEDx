import json
from jsonschema import validate, Draft4Validator
from pathlib import Path

# Define file paths
base_path = Path(__file__).parent

#### SCHEMA FILE
#schema_file_path = base_path / "newFiles" / "job_schema.json"
schema_file_path = base_path / "newFiles" / "worker.jschema"
#schema_file_path = base_path / "newFiles" / "organization_schema.json"


#### JSON FILE
#instance_file_path = base_path / "newFiles" / "job-synthetic-example1_v1.json"
instance_file_path = base_path / "newFiles" / "worker-synthetic-example1_v1.json"
# = base_path / "newFiles" / "organization-example_v1.json"

# Load the schema file
with open(schema_file_path) as schema_file:
    schema_data = json.load(schema_file)
    schema = schema_data
    
# Extract the schema for the POST function
# schema = schemas[0]["requestBodySchema"]
# schema = schemas["requestBody"]

# Load the instance file
with open(instance_file_path) as instance_file:
    instance = json.load(instance_file)

# Create a Draft4Validator instance with the schema
validator = Draft4Validator(schema)

# Validate and collect errors, if any
errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

# Format error messages
for error in errors:
    print(f"Message     : {error.message}")
    print(f"Instance at : {'/'.join(map(str, error.path))}")
    print(f"Schema path : {'/'.join(map(str, error.schema_path))}")
    print("---------")

print("Done.")
