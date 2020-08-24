const interactions = require("./interactions");

async function doInteraction(interaction) {
  const start = Date.now();
  await interaction();
  console.log(`${interaction.name} took ${Date.now() - start} ms`);
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function scheduleInteractions() {
  while (true) {
    // perform random interaction
    await doInteraction(
      interactions[Math.floor(Math.random() * interactions.length)]
    );

    // wait some time, between half a second to five seconds between interactions
    await delay(500 + Math.floor(Math.random() * 4500));
  }
}

scheduleInteractions();
