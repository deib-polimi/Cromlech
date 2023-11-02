import yaml
import sys

def translate_to_tosca(yaml_data):
    # Parse the YAML string into a Python dictionary
    operations_data = yaml.safe_load(yaml_data)

    # Start the TOSCA topology template
    tosca_template = "tosca_definitions_version: tosca_simple_yaml_1_3\n\n"
    tosca_template += "topology_template:\n"
    tosca_template += "  node_templates:\n"

    # Loop through each operation in the parsed data
    for operation in operations_data['operations']:
        # Add each operation as a node template in TOSCA
        tosca_template += f"    {operation['name']}:\n"
        tosca_template += "      type: it.polimi.cromlech.operation\n"
        tosca_template += "      properties:\n"
        tosca_template += f"        consistency: {operation['consistency']}\n"
        tosca_template += f"        frequency: {operation['frequency']}\n"

     
            
        # Process database access
        tosca_template += "        database_access:\n"
        for access in operation['database_access']:
            entity_name = access['entity_name']
            tosca_template += f"          - entity_name: {entity_name}\n"
            read_attrs = access.get('read_attributes', [])
            if read_attrs:
                tosca_template += "            read_attributes:\n"
                for attr in read_attrs:
                    tosca_template += f"              - {attr}\n"
            write_attrs = access.get('write_attributes', [])
            if write_attrs:
                tosca_template += "            write_attributes:\n"
                for attr in write_attrs:
                    tosca_template += f"              - {attr}\n"
        
        # If there are forced_operations, add them as requirements
        if list(filter(lambda x: x, operation['forced_operations'])):
            tosca_template += "      requirements:\n"
            for forced_op in operation['forced_operations']:
                tosca_template += f"        - forced_operations:\n"
                tosca_template += f"            node: {forced_op}\n"
                tosca_template += "            relationship: it.polimi.cromlech.forced_operation_relationship\n"


    # Return the TOSCA template string
    return tosca_template

filename = sys.argv[1]
with open(filename, 'r') as f:
    # Convert the YAML snippet to a TOSCA topology template
    tosca_topology_template = translate_to_tosca(f.read())
    with open(f"{filename.split('.')[0]}-TOSCA.yaml", 'w') as f2:
            f2.write(tosca_topology_template)