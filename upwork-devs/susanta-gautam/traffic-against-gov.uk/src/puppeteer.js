const puppeteer = require('puppeteer');
const path = require('path')
const logger = require('./logger')
const {get_links, download_pdf, pdfProcessor} = require('./functions')

const generateTraffic = async(URL) => {
    const browser = await puppeteer.launch({
        headless: true,
        ignoreHTTPSErrors: true,
        args: ["--no-sandbox"]
    });
    const page = await browser.newPage();
    logger.log('info', "Loading URL: " +URL);

    await page.goto(URL);
    await page.$eval('input[title="Search"]', el => el.value = 'pdf');
    await page.evaluate(() => {
        let elements = document.getElementsByClassName('gem-c-search__submit');
        for (let element of elements) {
            element.click()
        }
    });
    await page.waitForSelector('#order');

    // GEt all the links that allows us to download the pdf files from the Page. Here the string "download-pdf-version" is passed 
    // as i have found that all the links that allows us to download have that in url
    links = await get_links(page, "download-pdf-version")

    for (let index = 0; index<links.length; ++index) {
        logger.log('info', "Navigating to the URL: " + links[index])
        await page.goto(links[index])
        await page.waitForSelector('#search-box')

        // Now let's grab the link for the the site that contains .pdf extension.
        const pdf_link = await get_links(page, ".pdf");
        logger.log('info', "Link from which the pdf will be downloaded is: " +pdf_link);
        const split_link = pdf_link[0].split("/");
        pdf_name = split_link[(split_link.length) - 1]


        // Get the directory to save the pdf.
        split_url = URL.split("/")
        directory_to_save = split_url[(split_url.length) - 1]

        // Function call to download the pdf file.
        await download_pdf(pdf_link[0], pdf_name, directory_to_save)


        // Get the pdf location to process the pdf
        pdf_file = path.join(__dirname, '../' + directory_to_save + '/' + pdf_name)
        
        // Process the pdf to find if the pdf is Glasswall Approved or not.
        logger.log('info', "Processing PDF: "+pdf_name)
        await pdfProcessor(pdf_file, URL)
        
    }

    browser.close()
    logger.log('info', 'Task Completed. Shutting Down Node Server.')
}

module.exports = generateTraffic