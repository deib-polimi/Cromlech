const process = require('process');
const parser = require('./parser');

const appName = process.argv[2] || 'example-app'
const communicationWeight = process.argv[3] || 1
const couplingWeight = process.argv[4] ||  10
const numMicroservices = process.argv[5] ||  2

console.log(communicationWeight)
parser.parse(appName, 'master',
    'js', communicationWeight, couplingWeight, numMicroservices).then(() => {
    console.log('DONE!')
    process.exit()
})
