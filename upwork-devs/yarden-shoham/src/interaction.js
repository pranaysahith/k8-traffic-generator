const Utils = require("./utils");

class Interaction {
  execute = async () => {};

  static async time({ name, interaction }) {
    const start = Date.now();
    await new interaction().execute();
    console.log(`"${name}" took ${Date.now() - start} ms`);
  }

  static async schedule(interactionsWithNames) {
    while (true) {
      // perform random interaction
      await this.time(
        interactionsWithNames[
          Math.floor(Math.random() * interactionsWithNames.length)
        ]
      );

      // wait up to one second between interactions
      await Utils.delay(Math.floor(Math.random() * 1000));
    }
  }
}

module.exports = Interaction;
