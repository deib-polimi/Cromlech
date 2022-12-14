import yaml
import json
import sys

# Process relations for a single entity
def process_entity_relations(entity_name, description_data, out_file):
    relations = description_data['relations']
    first = True
    for rel in relations:
        if rel['origin'] == entity_name:
            if first:
                out_file.write(' * relations:\n')
                first = False
            out_file.write(' *   - entity_name: ' + rel['destination'] + '\n')
            out_file.write(' *     type: ' + rel['type'] + '\n')    

# Process db accesses for a single operation
def process_db_accesses(db_accesses, out_file):
    out_file.write(' * entities:\n')
    for db_access in db_accesses:
        name = db_access['entity_name']
        out_file.write(' *   - entity_name: ' + name + '\n')
        access_mode = 'write' if 'write_attributes' in db_access.keys() else 'read'
        out_file.write(' *     access_mode: ' + access_mode + '\n')
        
# Process a single operation
def process_operation(operation, out_file):
    out_file.write('/**\n')
    out_file.write(' * @Operation\n')
    
    name = operation['name']
    out_file.write(' * name: ' + name + '\n')
        
    consistency = 'low' if operation['consistency'] == 'L' else 'high'
    out_file.write(' * integrity: ' + consistency + '\n')

    frequency = operation['frequency']
    out_file.write(' * frequency: ' + str(frequency) + '\n')

    out_file.write(' * forced_entities:\n')
    out_file.write(' *   -\n') # TODO va bene lasciare sempre vuoto?

    db_accesses = operation['database_access']
    process_db_accesses(db_accesses, out_file)

    out_file.write(' */\n\n')

# Peocess a single entity of an operation
def process_entity(op_entity, entities):
    attributes = set()
    if 'read_attributes' in op_entity.keys():
        for attr in op_entity['read_attributes']:
            attributes.add(attr)
    if 'write_attributes' in op_entity.keys():
        for attr in op_entity['write_attributes']:
            attributes.add(attr)

    name = op_entity['entity_name']
    if name in entities.keys():
        entities[name].update(attributes)
    else:
        entities[name] = attributes

# Print entities to file
def print_entities(entities, description_data, out_file):
    for e in entities.keys():
        out_file.write('/**\n')
        out_file.write(' * @Entity\n')
        out_file.write(' * name: ' + e + '\n')
        out_file.write(' * implementation: ' + e + '\n')
        out_file.write(' * replication_overhead: 1\n') # TODO possiamo cambiare valore?
        out_file.write(' * columns:\n')
        for attr in entities[e]:
            out_file.write(' *   - ' + attr + '\n')
        process_entity_relations(e, description_data, out_file)
        out_file.write(' */\n\n')
    
# Process the list of entities
def process_entities(yaml_data, desxription_data, out_file):
    entities = {}
    for operation in yaml_data['operations']:
        for op_entity in operation['database_access']:
            process_entity(op_entity, entities)

    print_entities(entities, description_data, out_file)
        
# Process the list of operations
def process_operations(yaml_data, out_file):
    for operation in yaml_data['operations']:
        process_operation(operation, out_file)

if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'cromlech_input.yaml'
    input_file = open(input_path, 'r')
    yaml_data = yaml.safe_load(input_file)
    input_file.close()

    description_path = sys.argv[2] if len(sys.argv) > 2 else 'sc_description_input.json'
    description_file = open(description_path, 'r')
    description_data = json.load(description_file)
    description_file.close()
    
    output_path = sys.argv[3] if len(sys.argv) > 3 else 'output.txt'
    output_file = open(output_path, 'w')
    process_entities(yaml_data, description_data, output_file)
    process_operations(yaml_data, output_file)
    output_file.close()
