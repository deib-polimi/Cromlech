

import json
import sys

def translate(input_file_path, output_file_path):
    # Read the input JSON file
    with open(input_file_path, 'r', encoding='utf-8-sig') as f:
        first_json_data = json.load(f)
    
    # Initialize the second JSON format
    second_json_format = {
        "communication_weight": 0.5,
        "coupling_weight": 0.5,
        "microservices": []
    }
    
    # Initialize counters for entity and operation IDs
    entity_counter = 0
    operation_counter = 0
    
    # Populate the 'microservices' field
    for idx, service in enumerate(first_json_data['services']):
        # Extract entities from 'nanoentities', remove attribute names, and assign IDs
        entities = list(set([entity.split('.')[0] for entity in service['nanoentities']]))
        entities_with_id = [{"id": f"e{entity_counter + i}", "label": entity} for i, entity in enumerate(entities)]
        entity_counter += len(entities)
        
        microservice = {
            "id": f"m{idx}",
            "label": f"M{idx}",
            "entities": entities_with_id,
            "operations": []
        }
        
        # Bind operations from 'useCaseResponsibility' based on service names
        if service['name'] in first_json_data['useCaseResponsibility']:
            for use_case in first_json_data['useCaseResponsibility'][service['name']]:
                microservice["operations"].append({
                    "id": f"op{operation_counter}",
                    "label": use_case
                })
                operation_counter += 1
        
        second_json_format["microservices"].append(microservice)
    
    # Save the converted JSON to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(second_json_format, f, indent=4)


if __name__ == '__main__':
    translate(sys.argv[1], sys.argv[2])