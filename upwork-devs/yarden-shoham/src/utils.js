const crypto = require("crypto");
const fs = require("fs");

class Utils {
  static delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  static fileHash(filename, algorithm = "sha256") {
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
}

module.exports = Utils;
