const Interaction = require("./interaction");
const puppeteer = require("puppeteer");

class PricingColumnCountTest extends Interaction {
  browser = null;
  page = null;
  targetHost = null;
  priceColumns = null;

  execute = async () => {
    this.init();
    await this.setupBrowser();
    await this.openPage();
    await this.findPriceColumns();
    this.checkPriceColumnCount();
    await this.closeBrowser();
  };

  init = () => {
    this.targetHost = process.env.TARGET_HOST
      ? process.env.TARGET_HOST
      : "glasswallsolutions.com";
  };

  setupBrowser = async () => {
    this.browser = await puppeteer.launch({ args: ["--no-sandbox"] });
  };

  openPage = async () => {
    this.page = await this.browser.newPage();
    this.page.setViewport({ width: 1920, height: 1080 });
    await this.page.goto(`http://${this.targetHost}/pricing/`, {
      waitUntil: "networkidle2",
    });
  };

  findPriceColumns = async () => {
    this.priceColumns = await this.page.$$(".pricing_col");
  };

  checkPriceColumnCount = () => {
    console.assert(this.priceColumns.length === 3);
  };

  closeBrowser = async () => {
    await this.browser.close();
  };
}

module.exports = PricingColumnCountTest;
