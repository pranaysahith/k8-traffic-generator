const puppeteer = require("puppeteer");
const fs = require("fs");
const http = require("http");
const crypto = require("crypto");

const targetHost = process.env.TARGET_HOST || "glasswallsolutions.com";

function fileHash(filename, algorithm = "sha256") {
  return new Promise((resolve, reject) => {
    // Algorithm depends on availability of OpenSSL on platform
    // Another algorithms: 'sha1', 'md5', 'sha256', 'sha512' ...
    let shasum = crypto.createHash(algorithm);
    try {
      let s = fs.ReadStream(filename);
      s.on("data", function (data) {
        shasum.update(data);
      });
      // making digest
      s.on("end", function () {
        const hash = shasum.digest("hex");
        return resolve(hash);
      });
    } catch (error) {
      return reject("calc fail");
    }
  });
}

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
    (await fileHash(filename)) ===
      "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  );

  fs.unlink(filename, (err) => {
    if (err) console.error(err);
  });

  await browser.close();
};

module.exports = [pdfTest];
