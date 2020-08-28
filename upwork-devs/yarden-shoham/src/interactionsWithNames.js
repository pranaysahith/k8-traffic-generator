const PdfTest = require("./pdfTest");
const PricingCountTest = require("./pricingCountTest");
const PricingColumnCountTest = require("./pricingColumnCountTest");

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
];
