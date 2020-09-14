const fs = require('fs');
const fetch = require('node-fetch')
const PdfReader = require('pdf2json')
const https = require('https')
const path = require('path')
const logger = require('./logger')



const get_links = async(page, selectString) => {
    list = [];

    const hrefs = await page.$$eval('a', links => links.map(a => a.href));
    hrefs.forEach(function async(link){
        if( link.includes(selectString)){
            list.push(link)
        }
    })
    return list;
}


const httpsAgent = new https.Agent({
    rejectUnauthorized: false
})


const download_pdf = async(urlSting, name, save_location) => {
    logger.log('info', "Downloading PDF from URL: " + urlSting)
    
    try {
        const res = await fetch(urlSting, {
            agent: httpsAgent
        });

        if (fs.existsSync(path.join(__dirname, "../"+ save_location)) == false){
            logger.log('info', `Creating directory ${path.join(__dirname, "../"+ save_location)}`)
            fs.mkdir(path.join(__dirname, "../"+ save_location), function(err) {
                if(err) {
                    logger.log('error', "Could not create directory.")
                }else {
                    logger.log('info', "Directory created successfully.")
                }

            })
        }

        save_to = path.join(__dirname, "../"+save_location+"/"+name)
        logger.log('info', "Saving the pdf to location: "+save_to)
        const pdfStream = fs.createWriteStream(save_to)
        await new Promise((resolve, reject) => {
            res.body.pipe(pdfStream);
            res.body.on("error", (err) => {
                reject(err);
            });
            pdfStream.on("finish", function() {
                resolve()
            })
        })
    } catch {
        logger.log('error', 'Error while downloading file with name: ' + name)
    }
    
}


const pdfProcessor = (filename, downloadURL) => {
    
    try {
    
        const pdfParser = new PdfReader(this, 1);

        pdfParser.on("pdfParser_dataError", errData => console.error(errData.parserError));
        pdfParser.on("pdfParser_dataReady", pdfData => {
            if((pdfParser.getRawTextContent()).includes("Glasswall Approved")){
                logger.log('info', `Pdf file ${filename} downloaded form ${downloadURL} is tagged with Glasswall Approved.`)
            } else {
                logger.log('info', `Pdf file ${filename} downloaded form ${downloadURL} is not tagged with Glasswall Approved.`)
            }
        })
        pdfParser.loadPDF(filename)
        return process

    } catch {
        logger.log('error', 'Could not process the file: ' +filename)
    }
}



module.exports = {
    get_links,
    download_pdf,
    pdfProcessor
}