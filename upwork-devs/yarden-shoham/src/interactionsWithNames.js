const PdfTest = require("./pdfTest");
const PricingCountTest = require("./pricingCountTest");
const PricingColumnCountTest = require("./pricingColumnCountTest");
const RandomClickInteraction = require("./randomClickInteraction");

module.exports = [
  {
    name: "Check PDF is downloadable and correct",
    interaction: PdfTest,
  },
  {
    name: "Check there are at least 8 prices listed",
    interaction: PricingCountTest,
  },
  {
    name: "Check there are exactly 3 price columns (plans) listed",
    interaction: PricingColumnCountTest,
  },
  {
    name: "Click a random button",
    interaction: RandomClickInteraction,
  },
];
