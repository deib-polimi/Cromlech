import json
import codecs
import sys
from pangaea.pangaea_artefact.output_converter.output_converter import convert
from translate_sc2pangaea import translate as sc2pangea_translate
from translate_sc2cromlech import translate as sc2cromlech_translate
from similarity import compute_similarity

app = sys.argv[1]
sc_output = sys.argv[2]
alpha = float(sys.argv[3])


if app == "TRAINTICKET":
    cr_architecture = "./input/trainticket_no_trans_cromlech.yaml"
    similarity_reference_output = "./results/manual_trainticket/manual_trainticket.txt"
elif app == "TUTORED":
    cr_architecture = "./input/tutored2_cromlech.yaml"
    similarity_reference_output = "./results/manual_tutored/manual_tutored.txt"
else: raise Exception("INVALID APP")

pangea_translated_output = "./results/temp/pangea_translated_output.json"
cr_translated_output = "./results/temp/cr_translated_output.json"


sc2pangea_translate(sc_output, pangea_translated_output)
results = convert(cr_architecture, pangea_translated_output, alpha=alpha)


with open(sc_output, "r+b") as fp:
    s = fp.read()
    if s.startswith(codecs.BOM_UTF8):
        u = s.decode("utf-8-sig")
        s = u.encode("utf-8")
    sc_output_data = json.loads(s)



use_case_responsibility_dict = sc_output_data.get('useCaseResponsibility', {})
sc_services = list(use_case_responsibility_dict.values())


cr_translated_output_data = sc2cromlech_translate(cr_architecture, sc_services)
with open(cr_translated_output, 'w') as file:
    file.write(str(cr_translated_output_data))

results["operation_similarity"], results["data_similarity"] = compute_similarity(cr_translated_output, similarity_reference_output)

print(json.dumps(results, indent=4))

