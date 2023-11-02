import yaml
import sys
from collections import OrderedDict

def translate_from_tosca(tosca_data):
    # Load the TOSCA template data
    tosca_template = yaml.safe_load(tosca_data)

    # This will hold the operations in an ordered format
    operations = []

    # Loop through node templates in the TOSCA topology
    for node_name, node in tosca_template.get('topology_template', {}).get('node_templates', {}).items():
        if node['type'] == 'it.polimi.cromlech.operation':
            operation = OrderedDict([('name', node_name)])
            operation.update(node.get('properties', {}))

            # Handle requirements (forced_operations)
            forced_operations = []
            for requirement in node.get('requirements', []):
                if 'forced_operations' in requirement:
                    forced_op = requirement['forced_operations']['node']
                    forced_operations.append(forced_op)
            operation['forced_operations'] = forced_operations

            # Handle database access
            database_access = []
            for access in node.get('attributes', {}).get('database_access', []):
                db_access_dict = OrderedDict()
                db_access_dict['entity_name'] = access['entity_name']
                read_attr = access.get('read_attributes', [])
                if read_attr:
                    db_access_dict['read_attributes'] = read_attr
                write_attr = access.get('write_attributes', [])
                if write_attr:
                    db_access_dict['write_attributes'] = write_attr
                database_access.append(db_access_dict)
            
            operation['database_access'] = database_access
        operations.append(operation)

    # Create the non-standard format dictionary
    non_standard_format = OrderedDict([('operations', operations)])
    return non_standard_format

def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

# Add custom representer for OrderedDict
yaml.add_representer(OrderedDict, represent_ordereddict)

# Read the TOSCA YAML file
input_filename = sys.argv[1]
output_filename = sys.argv[2]
with open(input_filename, 'r') as f:
    # Convert TOSCA topology template to non-standard format
    non_standard_data = translate_from_tosca(f.read())
    with open(output_filename, 'w') as f2:
        yaml.dump(non_standard_data, f2, default_flow_style=False)

