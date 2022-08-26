out_file = open('microservices-data.js', 'w')

out_file.write('let result = ')
microservices_file = open('microservices.json', 'r')
for line in microservices_file:
    out_file.write(line)
microservices_file.close()
out_file.write('\n\n')

out_file.write('let entities_coupling = ')
coupling_file = open('entities_coupling.json', 'r')
for line in coupling_file:
    out_file.write(line)
coupling_file.close()
out_file.write('\n\n')

out_file.write('let entity_replication_cost = ')
replication_file = open('replication.json', 'r')
for line in replication_file:
    out_file.write(line)
replication_file.close()
out_file.write('\n\n')

template_file = open('microservices-data_template.js', 'r')
for line in template_file:
    out_file.write(line)
template_file.close()
out_file.write('\n\n')

out_file.close()
