const http = require('http');

const inputs = process.env.REQUEST_TYPES ? JSON.parse(process.env.REQUEST_TYPES) : require('./input.json');

const batchSize = process.env.BATCH_SIZE && (Number(process.env.BATCH_SIZE) < 1000) ? Number(process.env.BATCH_SIZE) : 1000;
const batchInterval = process.env.BATCH_INTERVAL && (Number(process.env.BATCH_INTERVAL) > 1000) ? Number(process.env.BATCH_INTERVAL) : 5000;
const requestTypes = []
let reqCounter = 0;
let resCounter = 0;
let errCounter = 0;
const resStatuses = {};

console.log(`Start LoadGenerator with batch size: ${batchSize} and batch interval: ${batchInterval}`);
console.log('REQUEST_TYPES:');
console.log(JSON.stringify(inputs));

setInterval(() => {
    const allResponses = errCounter + resCounter;
    console.log(`Number of request send: ${reqCounter}`)
    console.log(`Number of errors received: ${errCounter}`)
    console.log(`Number of succesful response received: ${resCounter}`)
    console.log(`Number of all response received: ${allResponses}`)
    console.log(`Response statuses: ${JSON.stringify(resStatuses)}`)
    console.log("\n")

    if (allResponses >= reqCounter) {
        startLoadGenerator();
    }

}, batchInterval)

// preparation
for (let ii = 0; ii < inputs.length; ii++) {
    const input = inputs[ii];

    requestTypes.push(input)
}

const startLoadGenerator = () => {
    requestTypes.forEach(reqType => {
        (() => {
            for (let j = 0; j < batchSize; j++) {
                reqCounter++;
                const req = http.request(reqType);
                req.end();
    
                req.on('response', (info) => {
                    resCounter++;
                    const statusCode = info.statusCode;
                    resStatuses[statusCode] ? resStatuses[statusCode]++ : resStatuses[statusCode] = 1;
                });
    
                const errFunc = (info) => {
                    errCounter++
                    //console.log(`Error: ${info}`);
                }
                req.on('error', errFunc);
                req.on('abort', errFunc);
                req.on('timeout', errFunc);
            }
        })()
    })
}

startLoadGenerator();
