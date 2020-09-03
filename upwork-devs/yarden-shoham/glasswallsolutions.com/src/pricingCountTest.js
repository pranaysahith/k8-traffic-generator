const Interaction = require("./interaction");
const puppeteer = require("puppeteer");

class PricingCountTest extends Interaction {
  browser = null;
  page = null;
  targetHost = null;
  prices = null;

  execute = async () => {
    this.init();
    await this.setupBrowser();
    await this.openPage();
    await this.findPrices();
    this.checkPriceCount();
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

  findPrices = async () => {
    this.prices = await this.page.$$(".price");
  };

  checkPriceCount = () => {
    console.assert(this.prices.length >= 8);
  };

  closeBrowser = async () => {
    await this.browser.close();
  };
}

module.exports = PricingCountTest;
