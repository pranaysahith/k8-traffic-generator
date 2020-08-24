const interactions = require("./interactions");
const Utils = require("./utils");

async function doInteraction(interaction) {
  const start = Date.now();
  await interaction();
  console.log(`${interaction.name} took ${Date.now() - start} ms`);
}

async function scheduleInteractions() {
  while (true) {
    // perform random interaction
    await doInteraction(
      interactions[Math.floor(Math.random() * interactions.length)]
    );

    // wait some time, between half a second to five seconds between interactions
    await Utils.delay(500 + Math.floor(Math.random() * 4500));
  }
}

scheduleInteractions();
