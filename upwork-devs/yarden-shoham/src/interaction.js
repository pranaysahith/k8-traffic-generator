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

      // wait some time, between half a second to five seconds between interactions
      await Utils.delay(500 + Math.floor(Math.random() * 4500));
    }
  }
}

module.exports = Interaction;
