const logger = require('./logger')
const generateTraffic = require('./puppeteer')

const URL = process.env.URL


async function runLoop() {
    startdate = (Date.now() - 1000)
    logger.log("info", 'Started the loop')
    while((Date.now() - startdate) < (process.env.RUNFORMINUTE * 60000)) {
        await generateTraffic(URL);
    }
}
    
runLoop()        
