const csv = require('csv-parser')
const fs = require('fs')

async function parseCSV(path) {
    const results = [];
    return new Promise((resolve, reject) => {
        fs.createReadStream(path)
            .pipe(csv())
            .on('data', (data) => {
                results.push(data)
            })
            .on('end', () => {
                resolve(results);
            });
    })
}

async function writeCSV(fileName, header, rows) {
    const csvWriter = createCsvWriter({
        append: true,
        path: fileName + '.csv',
        header
    });
    await csvWriter.writeRecords(rows);
}

module.exports = {
    parseCSV,
    writeCSV
}
