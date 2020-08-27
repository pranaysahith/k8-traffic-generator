const PdfTest = require("./pdfTest");
const PricingCountTest = require("./pricingCountTest");

module.exports = [
  {
    name: "Check PDF is downloadable and correct",
    interaction: PdfTest,
  },
  {
    name: "Check there are at least 8 prices listed",
    interaction: PricingCountTest,
  },
];
