(() => {
  const form = document.getElementById("expense-form");
  if (!form) {
    return;
  }

  const PLACEHOLDERS = { percentage: "%", exact: "PLN" };

  const participantBoxes = form.querySelectorAll('input[name="participants"]');
  const amountInput = form.querySelector('input[name="amount"]');
  const summary = document.getElementById("split-summary");
  const hint = document.getElementById("split-hint");

  const parseNumber = (value) => {
    const parsed = parseFloat(String(value).replace(",", "."));
    return Number.isNaN(parsed) ? 0 : parsed;
  };

  const currentSplit = () => form.querySelector('input[name="split_type"]:checked').value;
  const shareInputOf = (box) => form.querySelector(`input[name="share_${box.value}"]`);
  const format = (value) => (Math.round(value * 100) / 100).toString();

  const describeSummary = (split, activeBoxes) => {
    const amount = parseNumber(amountInput.value);
    if (split === "equal") {
      const perPerson = activeBoxes.length > 0 ? amount / activeBoxes.length : 0;
      return { text: window.t("summary.perPerson", { value: perPerson.toFixed(2) }), state: "" };
    }
    const sum = activeBoxes.reduce((total, box) => total + parseNumber(shareInputOf(box).value), 0);
    const target = split === "percentage" ? 100 : amount;
    const unit = split === "percentage" ? "%" : "PLN";
    const matches = Math.abs(sum - target) < 0.005 && target > 0;
    return {
      text: `${format(sum)} / ${format(target)} ${unit}`,
      state: matches ? "ok" : "warn",
    };
  };

  const refresh = () => {
    const split = currentSplit();
    const activeBoxes = [...participantBoxes].filter((box) => box.checked);
    participantBoxes.forEach((box) => {
      const input = shareInputOf(box);
      input.hidden = split === "equal";
      input.disabled = split === "equal" || !box.checked;
      input.placeholder = PLACEHOLDERS[split] || "";
      box.closest(".participant").classList.toggle("is-off", !box.checked);
    });
    const { text, state } = describeSummary(split, activeBoxes);
    summary.textContent = text;
    summary.dataset.state = state;
    hint.textContent = window.t(`hint.${split}`);
  };

  form.addEventListener("input", refresh);
  form.addEventListener("change", refresh);
  document.addEventListener("langchange", refresh);
  refresh();
})();