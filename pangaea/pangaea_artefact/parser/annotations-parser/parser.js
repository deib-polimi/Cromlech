const Util = require('./util')
const Rows = require('./rows')
const File = require('./file')
const regex = RegExp('/.md|index|util|\.xml|\.iml|\.gitignore|\.json|_|\.spec.js/');

const path = require('path')

const LOW_CONSISTENCY_VALUE = 1;
const HIGH_CONSISTENCY_VALUE = 5;
const READ_ACCESS_VALUE = 1;
const WRITE_ACCESS_VALUE = 2;
const COMPOSITION_RELATION_VALUE = 0;
const AGGREGATION_RELATION_VALUE = 1;
const FORCED_ENTITY_DEPENDENCY_VALUE = 150;

async function parse(repositoryName, branch, fileExtension, communication_weight = 1, coupling_weight = 8, num_microservices) {
    const entities = [];
    const operations = [];
    const entitiesTranslations = {};
    const operationsTranslations = {};
    const dependencies = {};
    const entities_coupling = {};

    const microservices = [];

    await setMicroservices(microservices, num_microservices)

    let files = [];

    let repo_directory = path.join(__dirname, '..', 'repository', repositoryName);
    // read all the files in directories recursively
    await Util.walk(repo_directory, fileExtension, regex, files);

    // cycle over those files, and extract entities and operations
    await extractEntitiesAndOperations(entities, operations, files)

    // translate Entities and Operations in format Ex - OPy
    await initializeTranslations(entities, entitiesTranslations, operations, operationsTranslations);

    // cycle over entities to get the coupling criteria with each other
    await prepareEntitiesCoupling(entities, entities_coupling, entitiesTranslations);

    // cycle over operations to get the dependency with each of the entities
    await prepareDependencies(dependencies, entities, operations, entitiesTranslations, operationsTranslations);

    // translate entities and operations list
    let translatedEntities = entities.map(e => translateEntity(entitiesTranslations, e.name));
    let translatedOperations = operations.map(op => translateOperation(operationsTranslations, op.name));
    let replication_overhead = entities.map(e => e.replication_overhead);

    // prepare rows to be written in the file
    let rows = await Rows.prepareRows(translatedEntities, translatedOperations, dependencies, entities_coupling, microservices, num_microservices, coupling_weight, replication_overhead, communication_weight)

    let timestamp = new Date().getTime();
    const fileName = repositoryName + "." + branch + "." + timestamp + ".dat"
    const filePath = path.join(__dirname, "..", 'input-files', fileName);

    // init file and write
    await File.prepareFile(filePath, rows);

    // parse result file CSV
    await File.parseResultCsv(dependencies, entitiesTranslations, operationsTranslations, entities_coupling);

    return {
        _id: repositoryName + "." + branch + "." + timestamp,
        entities,
        operations,
        entities_translations: entitiesTranslations,
        operations_translations: operationsTranslations,
        dependencies,
        entities_coupling,
        coupling_weight,
        communication_weight,
        replication_overhead,
        num_microservices,
    }
    }

async function initializeTranslations(entities, entitiesTranslations, operations, operationsTranslations) {
    await Promise.all(entities.map(async (e, index) => {
        entitiesTranslations[e.name] = "E" + (index + 1)
    }))
    await Promise.all(operations.map(async (op, index) => {
        operationsTranslations[op.name] = "OP" + (index + 1)
    }))
}

async function prepareEntitiesCoupling(entities, entities_coupling, entitiesTranslations) {
    // initialize array
    await Promise.all(entities.map(async (e, index) => {
        entities_coupling[translateEntity(entitiesTranslations, e.name)] = []
    }))
    // fill array of relations
    await Promise.all(entities.map(async (e) => {
        let relations = e.relations;
        if (relations !== undefined) {
            entities_coupling[translateEntity(entitiesTranslations, e.name)] = relations.map(r => {
                if (r.type.toLowerCase() === "aggregation") {
                    entities_coupling[translateEntity(entitiesTranslations, r.entity_name)].push({
                        entity_name: translateEntity(entitiesTranslations, e.name),
                        coupling: 1
                    })
                    return {
                        entity_name: translateEntity(entitiesTranslations, r.entity_name),
                        coupling: 1
                    }
                }
                else if (r.type.toLowerCase() === "composition") {
                    try {
                        entities_coupling[translateEntity(entitiesTranslations, r.entity_name)].push({
                            entity_name: translateEntity(entitiesTranslations, e.name),
                            coupling: 0
                        })
                        return {
                            entity_name: translateEntity(entitiesTranslations, r.entity_name),
                            coupling: 0
                        }
                    } catch(e){
                        console.error(r.entity_name)
                        throw e
                    }

                }
            }).filter(a => a != null)
        }
        entities_coupling[translateEntity(entitiesTranslations, e.name)].push({
            entity_name: translateEntity(entitiesTranslations, e.name),
            coupling: 2
        });
    }))
    // filling and sorting
    await Promise.all(entities.map(async (e, index) => {
        // fill missing entities
        await Promise.all(entities.map(async (e1, index) => {
            let translatedName = translateEntity(entitiesTranslations, e1.name);
            let found = false;
            entities_coupling[translateEntity(entitiesTranslations, e.name)].forEach(c => {
                if (c.entity_name === translatedName) {
                    found = true;
                }
            })
            if (!found) {
                entities_coupling[translateEntity(entitiesTranslations, e.name)].push({
                    entity_name: translatedName,
                    coupling: 2
                })
            }
        }));
        // sort by entity name
        entities_coupling[translateEntity(entitiesTranslations, e.name)].sort((a, b) => {
            let numA = parseInt(a.entity_name.substring(1));
            let numB = parseInt(b.entity_name.substring(1));
            return numA - numB;
        })
    }));

}

async function prepareDependencies(dependencies, entities, operations, entitiesTranslations, operationsTranslations) {
    // initialize array
    await Promise.all(operations.map(async (op, index) => {
        dependencies[translateOperation(operationsTranslations, op.name)] = entities.map(e => {
            return {
                entity_name: translateEntity(entitiesTranslations, e.name),
                dependency: 0
            }
        })
    }))
    await Promise.all(operations.map(async (op) => {
        let dbAccess = op.entities;
        let frequency = op.frequency;
        let integrity = op.integrity === "low" ? LOW_CONSISTENCY_VALUE : HIGH_CONSISTENCY_VALUE;
        let op_id = translateOperation(operationsTranslations, op.name);
        dependencies[translateOperation(operationsTranslations, op.name)] = dbAccess.map(db => {
            let accessFactor = 0;
            if (db.access_mode === 'read-write' || db.access_mode === 'write') {
                accessFactor = WRITE_ACCESS_VALUE;
            } else if ( db.access_mode === 'read') {
                accessFactor = READ_ACCESS_VALUE;
            }
            let dependencyFactor = accessFactor * frequency * integrity;
            if (op.forced_entities && op.forced_entities.length > 0 && op.forced_entities.indexOf(db.entity_name) !== -1){
                dependencyFactor = FORCED_ENTITY_DEPENDENCY_VALUE
            }
            return {
                entity_name: translateEntity(entitiesTranslations, db.entity_name),
                dependency: op.forced_entiti === db.entity_name ? FORCED_ENTITY_DEPENDENCY_VALUE : dependencyFactor
            }
        });
        // fill missing operations
        await Promise.all(entities.map(async (e) => {
            let translatedName = translateEntity(entitiesTranslations, e.name);
            let found = false;
            dependencies[translateOperation(operationsTranslations, op.name)].forEach(d => {
                if (d.entity_name === translatedName) {
                    found = true;
                }
            })
            if (!found) {
                dependencies[translateOperation(operationsTranslations, op.name)].push({
                    entity_name: translatedName,
                    dependency: 0
                })
            }
        }));
        // sort by entity name
        dependencies[translateOperation(operationsTranslations, op.name)].sort((a, b) => {
            try {
                let numA = parseInt(a.entity_name.substring(1));
                let numB = parseInt(b.entity_name.substring(1));
                return numA - numB;
            } catch(e){
                console.log(op.name)
                console.log(a,b);
                throw e;
            }

        })
    }))
}

function translateEntity(entitiesTranslations, name) {
    return entitiesTranslations[name];
}

function translateOperation(operationsTranslations, name) {
    return operationsTranslations[name];
}

function setMicroservices(microservices, num){
    for (let i = 0; i < num; i++){
        microservices.push("M"+(i+1))
    }
}

async function extractEntitiesAndOperations(entities, operations, files){
    await Promise.all(files.map(async (file) => {
        let resources = await Util.readFile(file);
        entities.push(...resources.entities)
        entities.sort((a, b) => {
            if (a.name > b.name) {
                return 1;
            }
            if (b.name > a.name) {
                return -1;
            }
            return 0;
        });
        operations.push(...resources.operations)
        operations.sort((a, b) => {
            if (a.name > b.name) {
                return 1;
            }
            if (b.name > a.name) {
                return -1;
            }
            return 0;
        });
    }));
}

module.exports = {
    parse
}
