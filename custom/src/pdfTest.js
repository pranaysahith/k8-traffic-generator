const Interaction = require("./interaction");
const puppeteer = require("puppeteer");
const fs = require("fs");
const download = require("download-pdf");

const Utils = require("./utils");

class PdfTest extends Interaction {
  browser = null;
  page = null;
  targetHost = null;
  filename = null;

  execute = async () => {
    this.init();
    await this.setupBrowser();
    await this.openPage();
    await this.downloadFile();
    await this.checkHash();
    this.deleteFile();
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
    await this.page.goto(`http://${this.targetHost}/technology/`, {
      waitUntil: "networkidle2",
    });
  };

  downloadFile = async () => {
    const href = await this.page.evaluate((sel) => {
      return document.querySelector(sel).getAttribute("href");
    }, "a.btn_block");

    this.filename = `pdf${Date.now()}.pdf`;

    return new Promise((resolve, reject) => {
      download(
        href.replace("https", "http"),
        {
          directory: ".",
          filename: this.filename,
        },
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  };

  checkHash = async () => {
    console.assert(
      (await Utils.fileHash(this.filename)) ===
        "983d194eec3acb41e64eb1d71afea938535d67f107c6b781a52279b6078148e5"
    );
  };

  deleteFile = () => {
    fs.unlink(this.filename, (err) => {
      if (err) console.error(err);
    });
  };

  closeBrowser = async () => {
    await this.browser.close();
  };
}

module.exports = PdfTest;
