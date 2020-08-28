const Interaction = require("./interaction");
const puppeteer = require("puppeteer");

class RandomClickInteraction extends Interaction {
  browser = null;
  page = null;
  targetHost = null;

  execute = async () => {
    this.init();
    await this.setupBrowser();
    await this.openPage();
    await this.clickRandomly();
    await this.closeBrowser();
  };

  init = () => {
    this.targetHost = process.env.TARGET_HOST
      ? process.env.TARGET_HOST
      : "glasswallsolutions.com";
  };

  setupBrowser = async () => {
    this.browser = await puppeteer.launch({
      args: ["--no-sandbox"],
    });
  };

  openPage = async () => {
    this.page = await this.browser.newPage();
    this.page.setViewport({ width: 1920, height: 1080 });
    await this.page.goto(`http://${this.targetHost}`, {
      waitUntil: "networkidle2",
    });
  };

  clickRandomly = async () => {
    await this.page.$$eval("a[class^='btn'],a.button", (buttons) => {
      const selectedButton =
        buttons[Math.floor(Math.random() * buttons.length)];
      selectedButton.scrollIntoViewIfNeeded();
      selectedButton.click();
    });
    await this.page.waitFor(1000);
  };

  closeBrowser = async () => {
    await this.browser.close();
  };
}

module.exports = RandomClickInteraction;
