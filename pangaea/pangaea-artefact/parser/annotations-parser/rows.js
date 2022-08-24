function printDataHeader() {
    console.log("data;")
}

function getMicroservicesRows(rows, microservices, num_microservices) {
    let row = ["set MICROSERVICES :="]
    microservices.map(m => {
        row.push(m);
    })
    row.push(';')
    rows.push(row.join(' ') + '\n\n');
    rows.push("param num_microservices := " + num_microservices + " ;\n\n")
}

function getCommunicationWeightRow(rows, communication_weight) {
    rows.push("param communication_weight := " + communication_weight + " ;\n\n");
}

function getCouplingWeightRow(rows, coupling_weight) {
    rows.push("param coupling_weight := " + coupling_weight + " ;\n\n");
}

function getReplicationWeightRows(rows, entities, replication_overhead, row_wise = true) {
    let r = [];
    r.push(["param replication_overhead:"])
    let firstRow = ['   ']
    if (row_wise){
        entities.map(e => {
            firstRow.push(e);
        })
        firstRow.push(":=")
        r.push(firstRow);
        let row = ["C  "];
        let index = 0;
        entities.map(e => {
            row.push(replication_overhead[index]+ " ");
            index++;
        })
        r.push(row);
        for (let i = 0; i < r.length; i++) {
            let row = r[i];
            if (i === r.length - 1) {
                row.push(';\n')
            }
            rows.push(row.join(' ') + '\n');
        }
    } else {
        firstRow.push("C :=")
        r.push(firstRow)
        let row = [""];
        let index = 0;
        entities.map(e => {
            row.push(e + " " + replication_overhead[index] + "\n");
            index++;
        })
        r.push(row);
        for (let i = 0; i < r.length; i++) {
            let row = r[i];
            if (i === r.length - 1) {
                row.push(';\n')
            }
            rows.push(row.join(' ') + '\n');
        }
    }

}

function getEntitiesRows(rows, entities) {
    let row = ["set ENTITIES :="]
    entities.map(e => {
        row.push(e);
    })
    row.push(';')
    rows.push(row.join(' ') + '\n\n');
}

function getOperationsRows(rows, operations) {
    let row = ["set OPERATIONS :="]
    operations.map(op => {
        row.push(op);
    })
    row.push(';')
    rows.push(row.join(' ') + '\n\n');
}

function getDependenciesRows(rows, entities, operations, dependencies) {
    let r = [];
    r.push(["param dependencies:"])
    let firstRow = ['   ']
    entities.map(e => {
        firstRow.push(e);
    })
    firstRow.push(":=")
    r.push(firstRow);
    operations.map(op => {
        let op_name = op;
        let row = [op_name];
        dependencies[op_name].map(dep => {
            row.push(dep.dependency)
        })
        r.push(row);
    })
    for (let i = 0; i < r.length; i++) {
        let row = r[i];
        if (i === r.length - 1) {
            row.push(';\n')
        }
        rows.push(row.join(' ') + '\n');
    }
}

function getEntitiesCouplingRows(rows, entities, entities_coupling) {
    console.log('')
    let r = [];
    r.push(["param entities_coupling:"])
    let firstRow = ['   ']
    entities.map(e => {
        firstRow.push(e);
    })
    firstRow.push(":=")
    r.push(firstRow);
    entities.map(e => {
        let entity_name = e;
        let row = [entity_name];
        entities_coupling[entity_name].map(ec => {
            row.push(ec.coupling)
        })
        r.push(row);
    })
    for (let i = 0; i < r.length; i++) {
        let row = r[i];
        if (i === 1) {
            rows.push(row.join(' ') + '\n')
        } else {
            if (i === r.length - 1) {
                row.push(';\n')
            }
            rows.push(row.join('  ') + '\n');
        }
    }
}

async function prepareRows(entities, operations, dependencies, entities_coupling, microservices, num_microservices, coupling_weight, replication_overhead, communication_weight) {
    const rows = [];
    await getMicroservicesRows(rows, microservices, num_microservices);
    await getCommunicationWeightRow(rows, communication_weight);
    await getCouplingWeightRow(rows, coupling_weight);
    await getReplicationWeightRows(rows, entities, replication_overhead, true);
    await getEntitiesRows(rows, entities);
    await getOperationsRows(rows, operations);
    await getDependenciesRows(rows, entities, operations, dependencies)
    await getEntitiesCouplingRows(rows, entities, entities_coupling)
    return rows;
}

module.exports = {
    prepareRows
}
