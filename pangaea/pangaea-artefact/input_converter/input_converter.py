import json

# Process relations for a single entity
def process_entity_relations(entity, out_file):
    if not 'relations' in entity.keys():
        return

    relations = entity['relations']
    out_file.write(' * relations:\n')
    for rel in relations:
        rel_name = rel['entity_name']
        rel_type = rel['type']
        out_file.write(' *   - entity_name: ' + rel_name + '\n')
        out_file.write(' *     type: ' + rel_type + '\n')
        
# Process a single entity
def process_entity(entity, out_file):
    out_file.write('/**\n')
    out_file.write(' * @Entity\n')
    
    name = entity['name']
    out_file.write(' * name: ' + name + '\n')
        
    table_name = entity['table_name']
    out_file.write(' * implementation: ' + table_name + '\n')

    replication_weight = entity['replication_weight']
    out_file.write(' * replication_overhead: ' + str(replication_weight) + '\n')

    columns = entity['columns']
    out_file.write(' * columns:\n')
    for column in columns:
        out_file.write(' *   - ' + column + '\n')

    process_entity_relations(entity, out_file)
        
    out_file.write(' */\n\n')

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
        
    consistency = operation['consistency']
    out_file.write(' * integrity: ' + consistency + '\n')

    frequency = operation['frequency']
    out_file.write(' * frequency: ' + str(frequency) + '\n')

    forced_entity = operation['forced_entity']
    out_file.write(' * forced_entities:\n')
    out_file.write(' *   - ' + forced_entity + '\n')

    db_accesses = operation['database_access']
    process_db_accesses(db_accesses, out_file)

    out_file.write(' */\n\n')
    
# Process the list of entities
def process_entities(json_data, out_file):
    for entity in json_data['entities']:
        process_entity(entity, out_file)

# Process the list of operations
def process_operations(json_data, out_file):
    for operation in json_data['operations']:
        process_operation(operation, out_file)

if __name__ == "__main__":
    input_file = open('input_pangaea.json', 'r')
    json_data = json.load(input_file)
    input_file.close()

    output_file = open('output.txt', 'w')
    process_entities(json_data, output_file)
    process_operations(json_data, output_file)
    output_file.close()


