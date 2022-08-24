const fs = require('fs');
const path = require('path');
const doctrine = require('doctrine');
const yaml = require('js-yaml');
const Promise = require('bluebird');

async function walk(dir, fileExtension, blacklistRegexp, results) {
    let currentDir = {};
    fs.readdirSync(dir)
        .filter(function blacklist(file) {
            return !blacklistRegexp.test(file);
        }).forEach(function (file) {
        let
            filePath = path.join(dir, file),
            stat = fs.statSync(filePath);

        let exportName = path.basename(file, fileExtension).replace(/-([a-z])/g, function (g) {
            return g[1].toUpperCase();
        });

        // in case is a dir, recurse
        if (stat.isDirectory()) {
            currentDir[exportName] = walk(filePath, fileExtension, blacklistRegexp, results);
        } else {
	    console.log(filePath)
            results.push(filePath)
        }
    });
    return currentDir;
}


async function parseJsDocs(file, fn) {
    return new Promise((resolve, reject) => {
        fs.readFile(file, function (err, data) {
            if (err) {
                return err;
            }

            let js = data.toString();
            let regex = /\/\*\*([\s\S]*?)\*\//gm;
            let fragments = js.match(regex);
            let docs = [];
            if (!fragments) {
                resolve(docs);
            } else {
                for (let i = 0; i < fragments.length; i++) {
                    let fragment = fragments[i];
                    let doc = doctrine.parse(fragment, {unwrap: true});

                    docs.push(doc);
                    if (i === fragments.length - 1) {
                        resolve(docs);
                    }
                }
            }
        });
    });
}

function getSwagger(fragment) {

        return new Promise((resolve, reject) => {
            for (let i = 0; i < fragment.tags.length; i++) {
                let tag = fragment.tags[i];
                if (tag.title === 'Entity' || tag.title === 'Operation') {
                    try {
                        resolve(yaml.safeLoadAll(tag.description));
                    } catch(e){
                        console.log(fragment.tags[0].description)
                        reject(e)
                    }
                }
            }
            resolve(false);
        })

}

async function readJsDoc(file) {
    let docs = await parseJsDocs(file);
    let resources = {
        entities: [],
        operations: []
    };
    await Promise.all(docs.map(async (doc) => {
        let annotation = (await getSwagger(doc))[0];
        if (!annotation) {
            return false;
        }
        if (annotation.replication_overhead) {
            resources.entities.push(annotation);
        } else {
            resources.operations.push(annotation);
        }
    }));
    return resources;
}

async function readFile(file, fn) {
    // extension name
    let ext = path.extname(file);
    //if ('.ts' === ext) {
       return await readJsDoc(file, fn);
    //}
}

module.exports = {
    walk,
    readFile
}
