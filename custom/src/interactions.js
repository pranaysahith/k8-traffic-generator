const puppeteer = require("puppeteer");
const fs = require("fs");
const http = require("http");
const Utils = require("./utils");

const targetHost = process.env.TARGET_HOST || "glasswallsolutions.com";

pdfTest = async () => {
  const browser = await puppeteer.launch({ args: ["--no-sandbox"] });
  let page = await browser.newPage();
  page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`http://${targetHost}/technology/`, {
    waitUntil: "networkidle2",
  });
  const href = await page.evaluate((sel) => {
    return document.querySelector(sel).getAttribute("href");
  }, "a.btn_block");

  const filename = `pdf${Date.now()}.pdf`;

  const file = fs.createWriteStream(filename);
  http.get(href.replace("https", "http"), function (response) {
    response.pipe(file);
  });

  console.assert(
    (await Utils.fileHash(filename)) ===
      "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  );

  fs.unlink(filename, (err) => {
    if (err) console.error(err);
  });

  await browser.close();
};

module.exports = [pdfTest];
