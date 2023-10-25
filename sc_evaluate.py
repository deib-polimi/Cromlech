import sys
import json

from pangaea.pangaea_artefact.output_converter.output_converter import convert
from translate_sc2pangaea import translate as sc2pangea_translate
from translate_sc2cromlech import translate as sc2cromlech_translate
from similarity import compute_similarity

sc_output = "./results/sc_raw/trainticket/chinese.json"
cr_architecture = "./input/trainticket_no_trans_cromlech.yaml"
similarity_reference_output = "./results/manual_trainticket/manual_trainticket.txt"

pangea_translated_output = "./results/temp/pangea_translated_output.json"
cr_translated_output = "./results/temp/cr_translated_output.json"


sc2pangea_translate(sc_output, pangea_translated_output)
results = convert(cr_architecture, pangea_translated_output)


with open(sc_output, 'r') as file:
    sc_output_data = json.load(file)

use_case_responsibility_dict = sc_output_data.get('useCaseResponsibility', {})
sc_services = list(use_case_responsibility_dict.values())


cr_translated_output_data = sc2cromlech_translate(cr_architecture, sc_services)
with open(cr_translated_output, 'w') as file:
    file.write(str(cr_translated_output_data))

results["data_similarity"], results["operation_similarity"] = compute_similarity(similarity_reference_output, cr_translated_output)

print(json.dumps(results, indent=4))

