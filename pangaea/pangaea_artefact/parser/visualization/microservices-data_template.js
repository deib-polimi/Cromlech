let total_coupling_cost = 0;
let total_communication_cost = 0;
let total_replication_cost = 0;
let total_cost = 0;

let elements = [];

let microservices = result.microservices;
microservices.map(m => {
    elements.push({
        data: {
            id: m.id,
            label: m.label,
            type: 'microservice'
        }
    })
    if (m.entities) {
        m.entities.map(e => {
            elements.push(
                {data: {id: e.id, label: e.label, type: 'entity'}},
                {data: {source: m.id, target: e.id, type: 'entity'}}
            )
            // replication_cost
            total_replication_cost += parseInt(entity_replication_cost[e.id.toUpperCase()]);
            total_cost += parseInt(entity_replication_cost[e.id.toUpperCase()]);
        })
    }
    if (m.operations) {
        m.operations.map(op => {
            elements.push(
                {data: {id: op.id, label: op.label, type: 'operation'}},
                {data: {source: m.id, target: op.id, type: 'operation'}}
            )
        })
    }
    if (m.dependencies) {
        m.dependencies.map(dep => {
            elements.push(
                {data: {source: m.id, target: dep.id, label: dep.weight, type: 'microservice', arrow: 'triangle'}},
            )
        })
        // communication cost
        total_communication_cost += m.dependencies.map(d => d.weight).reduce((a, b) => a + b, 0)
        total_cost += m.dependencies.map(d => d.weight).reduce((a, b) => a + b, 0)
    }
    let coupled_entities = 0;
    let coupling_cost = 0;
    // cycle over entities in that microservice
    m.entities.map(e1 => {
        let coupling = entities_coupling[e1.id.toUpperCase()].filter(a => a.coupling > 0).map(a => a.entity_name.toLowerCase());
        m.entities.map(e2 => {
            if (e2.id !== e1.id && coupling.indexOf(e2.id) !== -1) {
                let c = entities_coupling[e1.id.toUpperCase()][parseInt(e2.id.substring(1))-1].coupling;
                coupled_entities += c
            }
        })
    })
    coupling_cost = coupled_entities * result.coupling_weight;
    total_coupling_cost += coupling_cost;
    total_cost += coupling_cost;
})
let coupling_factor = total_coupling_cost / result.coupling_weight;
console.log('COUPLING:', total_coupling_cost)
console.log('COMMUNICATION:', total_communication_cost)
console.log('REPLICATION:', total_replication_cost)
console.log('TOTAL', total_cost)


