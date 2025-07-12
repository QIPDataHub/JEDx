""" Python Script to Convert JSON Schema to Dot Notation/XPath Paths
Below is a script that:
•	Reads the worker_schema.json (and follows $ref for local and code-sets references).
•	Generates all property paths in dot notation or XPath (slashed).
•	The script produces a CSV with two columns:
	DotNotation (e.g., worker.name.firstName)
	XPath (e.g., worker/name/firstName)
Script """

import json
import os
import csv

# File paths
input_schema_path = r'../work-P2-2/newFiles/worker_paid_hours_report.jschema'
root_object = 'worker_paid_hours_report'
code_sets_path = r'../work-P2-2/newFiles/code-sets.json'
output_csv_path = r'./worker_paid_hours_report_paths.csv'

# Load JSON schema files
with open(input_schema_path, encoding='utf-8') as f:
    input_schema = json.load(f)
with open(code_sets_path, encoding='utf-8') as f:
    code_sets = json.load(f)

# Simple $ref resolver (only handles local and code-sets references in this example)
def resolve_ref(ref, root_schema, code_sets):
    if ref.startswith('#/'):
        parts = ref.lstrip('#/').split('/')
        sub = root_schema
        for part in parts:
            sub = sub[part]
        return sub
    elif ref.startswith('code-sets.json#/'):
        parts = ref.replace('code-sets.json#/', '').split('/')
        sub = code_sets
        for part in parts:
            sub = sub[part]
        return sub
    else:
        raise ValueError(f'Unknown $ref: {ref}')



def extract_paths(schema, prefix='', paths=None, root_schema=None, code_sets=None):
    if paths is None:
        paths = []
    if root_schema is None:
        root_schema = schema

    def is_leaf(subschema):
        if subschema.get('type') in ['string', 'number', 'integer', 'boolean', 'null']:
            return True
        if 'enum' in subschema:
            return True
        return False

    if 'allOf' in schema:
        for sub in schema['allOf']:
            extract_paths(sub, prefix, paths, root_schema, code_sets)
        return paths

    if 'properties' in schema:
        for prop, subschema in schema['properties'].items():
            path = f'{prefix}.{prop}' if prefix else prop

            # Resolve $ref
            if '$ref' in subschema:
                description = subschema.get('description', '')
                if description:
                    paths.append([path.split('.')[-1], subschema.get('type', ''), description, path])
                else:
                    ref_schema = resolve_ref(subschema['$ref'], root_schema, code_sets)
                    extract_paths(ref_schema, path, paths, root_schema, code_sets)
                continue

            # Handle objects
            if subschema.get('type') == 'object' or 'properties' in subschema:
                if 'properties' in subschema:
                    extract_paths(subschema, path, paths, root_schema, code_sets)
                else:
                    description = subschema.get('description', '')
                    paths.append([path.split('.')[-1], subschema.get('type', ''), description, path])
                continue

            # Handle arrays
            if subschema.get('type') == 'array':
                items = subschema.get('items', {})
                item_path = f'{path}[]'

                if '$ref' in items:
                    description = items.get('description', '')
                    if description:
                        paths.append([item_path.split('.')[-1].replace('[]',''), items.get('type', ''), description, item_path])
                    else:
                        ref_schema = resolve_ref(items['$ref'], root_schema, code_sets)
                        extract_paths(ref_schema, item_path, paths, root_schema, code_sets)
                elif items.get('type') == 'object' or 'properties' in items:
                    extract_paths(items, item_path, paths, root_schema, code_sets)
                else:
                    description = items.get('description', '')
                    paths.append([item_path.split('.')[-1].replace('[]',''), items.get('type', ''), description, item_path])
                continue

            # Handle primitive leaf
            if is_leaf(subschema):
                description = subschema.get('description', '')
                paths.append([path.split('.')[-1], subschema.get('type', ''), description, path])

    elif is_leaf(schema):
        description = schema.get('description', '')
        paths.append([prefix.split('.')[-1], schema.get('type', ''), description, prefix])

    return paths

# Extract property paths
root_schema_section = input_schema.get('definitions', {}).get(root_object, input_schema)
paths = extract_paths(root_schema_section, prefix=root_object, root_schema=input_schema, code_sets=code_sets)

# Option: To output as XPath instead of dot notation, just replace '.' with '/' and remove '[]'
# xpath_paths = [p.replace('.', '/').replace('[]', '') for p in paths]

""" # Write both formats to CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['DotNotation', 'XPath'])
    for d, x in zip(paths, xpath_paths):
        writer.writerow([d, x]) """
        
# Write dot format to CSV
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Type', 'Description', 'Path'])
    for name, dtype, description, d in paths:
        writer.writerow([name, dtype, description, d])    

print("Done! Output written to:", output_csv_path)
