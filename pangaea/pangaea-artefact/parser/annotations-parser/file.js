const fs = require('fs');
const path = require('path');
const csvUtils = require('./csv_utils');

async function init(filePath) {
    // Check if the file exists in the current directory.
    let fileExists = await fs.existsSync(filePath);
    if (fileExists) { // if it exists -> delete
        await fs.unlinkSync(filePath);
    }
    // create new file, and append first row
    await fs.writeFileSync(filePath, "data;\n\n", {flag: 'a'});
}

async function write(filePath, rows) {
    for (let i = 0; i < rows.length; i++) {
        await fs.appendFileSync(filePath, rows[i]);
    }
}

async function parseResultFile(dependencies, entitiesTranslations, operationsTranslations, entities_coupling, entities_replication_cost) {
    let contents = await fs.readFileSync('result.txt', 'utf8');
    let rows = contents.split(";").slice(1);
    let i = 0;
    let microservices = [];
    let communication_weight_input = 0;
    let coupling_weight_input = 0;
    let pos_entities = {};
    rows.map(async (row) => {
        if (row.includes('communication_overhead')) {
            await parseMicroservices(row, microservices);
        } else if (row.includes('communication_weight')) {
            communication_weight_input = await parseNumeric(row)
        } else if (row.includes('coupling_weight')) {
            coupling_weight_input = await parseNumeric(row, coupling_weight_input)
        } else if (row.includes('pos_entities')) {
            await parseEntities(row, pos_entities, microservices, entitiesTranslations)
        } else if (row.includes('pos_operations')) {
            await parseOperations(row, microservices, operationsTranslations);
        }
    })
    // cycle over microservices
    await addDependencies(microservices, dependencies, pos_entities);

    // cycle over microservices
    await addCouplingCost(microservices, entities_coupling, coupling_weight_input);

    // cycle over microservices
    // await addReplicaCost(microservices, entities_coupling, coupling_weight_input)
    // console.log(pos_entities);
    // console.log(JSON.stringify(microservices, null, 2))

    let object = {
        communication_weight: communication_weight_input,
        coupling_weight: coupling_weight_input,
        microservices: microservices
    }
    await fs.writeFileSync("./visualization/microservices.json", JSON.stringify(object, null, 2))
}

async function parseResultCsv(dependencies, entitiesTranslations, operationsTranslations, entities_coupling) {
    let csvFile = `result.csv`;
    let parsedCSV = await csvUtils.parseCSV(csvFile);
    let microservices = [];
    let communication_weight_input = 0;
    let coupling_weight_input = 0;
    let pos_entities = {};
    let rows = await Promise.all(parsedCSV.map((row) => {
        let label = row[0]
        if (label) {
            if (label.includes('COMMUNICATION WEIGHT')){
                communication_weight_input = row[1]
            }
            else if (label.includes("COUPLING WEIGHT")){
                coupling_weight_input = row[1]
            } else if (label.includes('MICROSERVICES')){
                for (let i=1; i<Object.keys(row).length; i++){
                    let obj = {
                        id: row[i].toLowerCase(),
                        label: row[i],
                        entities: [],
                        operations: [],
                        dependencies: []
                    }
                    microservices.push(obj);
                }
            } else if (label.includes("E")){
                if (!pos_entities[label.toLowerCase()]) {
                    pos_entities[label.toLowerCase()] = []
                }
                for (let i=1; i<Object.keys(row).length; i++){
                    if (row[i] === "1"){
                        pos_entities[label.toLowerCase()].push("m" + (i))
                        microservices[i - 1].entities.push({
                            id: label.toLowerCase(),
                            label: getKeyByValue(entitiesTranslations, label)
                        })
                    }
                }
            } else if (label.includes("OP")){
                for (let i=1; i<Object.keys(row).length; i++){
                    if (row[i] === "1"){
                        microservices[i - 1].operations.push({
                            id: label.toLowerCase(),
                            label: getKeyByValue(operationsTranslations, label)
                        })
                    }
                }

            }
        }
    }));
    // cycle over microservices
    await addDependencies(microservices, dependencies, pos_entities, communication_weight_input);

    // cycle over microservices
    // await addCouplingCost(microservices, entities_coupling, coupling_weight_input);

    // cycle over microservices
    await addReplicaCost(microservices, entities_coupling, coupling_weight_input)
    // console.log(pos_entities);
    // console.log(JSON.stringify(microservices, null, 2))

    let object = {
        communication_weight: communication_weight_input,
        coupling_weight: coupling_weight_input,
        microservices: microservices
    }
    let p = path.join(__dirname,'..','visualization','microservices.json')
    await fs.writeFileSync(p, JSON.stringify(object, null, 2))

    // write entities_coupling.json
    let p2 = path.join(__dirname,'..','visualization','entities_coupling.json')
    await fs.writeFileSync(p2, JSON.stringify(entities_coupling, null, 2))

    let replicas = {}

    Object.keys(entitiesTranslations).map(e => {
        replicas[entitiesTranslations[e]] = 1
    })
    // write replication.json
    let p3 = path.join(__dirname,'..','visualization','replication.json')
    await fs.writeFileSync(p3, JSON.stringify(replicas, null, 2))
    return object;
}


async function parseNumeric(row) {
    row = row.split(" ");
    return parseInt(row[2]);
}

async function parseCouplingCost(row) {
    let coupling_cost = 0;
    let start = row.indexOf("coupling_factor");
    row = row.substring(start).split("\n");
    row.map(r => {
        if (!r.includes(":=")) {
            let split = r.split("  ");
            let micro = split[0];
            if (micro !== "") {
                coupling_cost += parseInt(split[1]);
            }
        }
    })
    return coupling_cost;
}

async function parseMicroservices(row, microservices) {
    let start = row.indexOf("communication_overhead");
    row = row.substring(start).split("\n");
    row.map(r => {
        if (!r.includes(":=")) {
            let split = r.split("  ");
            let micro = split[0];
            if (micro !== "") {
                microservices.push({
                    id: micro.toLowerCase(),
                    label: micro,
                    entities: [],
                    operations: [],
                    dependencies: []
                })
            }
        }
    })
}

async function parseEntities(row, pos_entities, microservices, entitiesTranslations) {
    let start = row.indexOf("pos_entities");
    row = row.substring(start).split("\n");
    row.map(r => {
        if (r.includes("E")) {
            let split = r.split("  ").filter(s => s !== "").map(s => s.trim());
            let entity = split[0];
            split.map((s, index) => {
                if (index !== 0 && s === "1") {
                    if (!pos_entities[entity.toLowerCase()]) {
                        pos_entities[entity.toLowerCase()] = []
                    }
                    pos_entities[entity.toLowerCase()].push("m" + (index))
                    microservices[index - 1].entities.push({
                        id: entity.toLowerCase(),
                        label: getKeyByValue(entitiesTranslations, entity)
                    })
                }
            })
        }
    })
}

async function parseOperations(row, microservices, operationsTranslations) {
    let start = row.indexOf("pos_operations");
    row = row.substring(start).split("\n");
    row.map(r => {
        if (r.includes("OP")) {
            let split = r.split("  ").filter(a => a !== "");
            let operation = split[0]
            split.map((s, index) => {
                if (index !== 0 && s.trim() === "1") {
                    microservices[index - 1].operations.push({
                        id: operation.toLowerCase(),
                        label: getKeyByValue(operationsTranslations, operation)
                    })
                }
            })
        }
    })
}

async function addDependencies(microservices, dependencies, pos_entities, communication_weight) {
    microservices.map((m, index) => {
        // cycle over operations in that microservice
        m.operations.map(op => {
            let dep = dependencies[op.id.toUpperCase()]
            if (dep) {
                // get the weight of that dependency only if > 0
                dep = dep.filter(d => d.dependency > 0)
                dep.map(d => {
                    let entity_name = d.entity_name;
                    let micro_id = "m" + (index + 1);
                    // get positions for that entity
                    let position = pos_entities[entity_name.toLowerCase()];
                    // if entity is not in the current microservice, than add the weight
                    if (position && position.indexOf(micro_id) === -1) {
                        let o = op.id;
                        position.map(p => {
                            m.dependencies.push({
                                id: p,
                                weight: d.dependency * communication_weight
                            })
                        })

                    }

                })
            }
        })
        m.communication_cost = m.dependencies.map(d => d.weight).reduce((a, b) => a + b, 0)
    });
}

async function addCouplingCost(microservices, entities_coupling, coupling_weight) {
    microservices.map((m, index) => {
        let coupled_entities = 0;
        let coupling_cost = 0;
        // cycle over entities in that microservice
        m.entities.map(e1 => {
            let coupling = entities_coupling[e1.id.toUpperCase()].filter(a => a.coupling === 1).map(a => a.entity_name.toLowerCase());
            m.entities.map(e2 => {
                if (e1.id !== e2.id && coupling.indexOf(e2.id) !== -1) {
                    coupled_entities += 1;
                }
            })
        })
        m.coupling_cost = coupled_entities * coupling_weight;
    });
}

async function addReplicaCost(microservices, entities_replication_cost) {
    let replication_cost = 0;
    microservices.map((m1, index) => {
        microservices.map(m2 => {
            let m1_entities = m1.entities.map(e => e.id);
            let m2_entities = m2.entities.map(e => e.id);
            m1_entities.map(e1 => {
                if (m2_entities.indexOf(e1) !== -1) {
                    replication_cost += 1
                }
            })
        })
    });
}

function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}

async function prepareFile(filePath, rows = []) {
    await init(filePath);
    await write(filePath, rows);
}

module.exports = {
    prepareFile,
    parseResultFile,
    parseResultCsv
}
