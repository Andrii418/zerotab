const splitSelect = document.getElementById("split_type");
const shareInputs = document.querySelectorAll(".share-input");
const hint = document.getElementById("split-hint");

const HINTS = {
  equal: "Everyone ticked pays the same amount.",
  percentage: "Enter each participant's percentage. The total must be 100.",
  exact: "Enter each participant's amount. The total must equal the expense amount.",
};
const PLACEHOLDERS = { percentage: "%", exact: "PLN" };

function updateShareInputs() {
  const splitType = splitSelect.value;
  const isEqual = splitType === "equal";
  hint.textContent = HINTS[splitType];
  shareInputs.forEach((input) => {
    input.hidden = isEqual;
    input.disabled = isEqual;
    input.placeholder = PLACEHOLDERS[splitType] || "";
  });
}

if (splitSelect) {
  splitSelect.addEventListener("change", updateShareInputs);
  updateShareInputs();
}