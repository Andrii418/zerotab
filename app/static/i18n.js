(() => {
  const STORAGE_KEY = "zerotab-lang";
  const DEFAULT_LANG = "pl";
  const LOCALES = { pl: "pl-PL", en: "en-GB" };
  const root = document.documentElement;

  const dict = {
    pl: {
      "aria.lang": "Język",
      "aria.theme": "Motyw",
      "tagline": "Rozliczaj wspólne wydatki jak najmniejszą liczbą przelewów",

      "groups.title": "Twoje grupy",
      "groups.lead": "Notuj, kto za co zapłacił, dziel koszty sprawiedliwie i rozliczaj się jak najmniejszą liczbą przelewów.",
      "empty.title": "Nie ma jeszcze żadnych grup",
      "empty.text": "Dodaj osoby, a potem utwórz pierwszą grupę poniżej.",
      "newGroup.title": "Nowa grupa",
      "newGroup.name": "Nazwa grupy",
      "newGroup.placeholder": "np. Weekend w górach",
      "newGroup.members": "Członkowie",
      "newGroup.create": "Utwórz grupę",
      "newGroup.needPerson": "Najpierw dodaj przynajmniej jedną osobę.",
      "people.title": "Osoby",
      "people.placeholder": "Imię",
      "people.aria": "Imię osoby",
      "people.add": "Dodaj osobę",

      "group.back": "Wszystkie grupy",
      "group.delete": "Usuń grupę",
      "confirm.deleteGroup": "Usunąć tę grupę razem ze wszystkimi wydatkami?",
      "confirm.deleteExpense": "Usunąć ten wydatek?",

      "stats.total": "Wydano łącznie",
      "stats.perPerson": "Na osobę",
      "stats.expenses": "Wydatki",
      "stats.members": "Członkowie",

      "balances.title": "Bilanse",
      "balances.hint": "Na prawo od linii: grupa jest winna tej osobie. Na lewo: ta osoba jest winna grupie.",
      "settlement.title": "Rozliczenie",
      "settlement.pays": "płaci",
      "settlement.done": "Wszystko rozliczone.",

      "expenses.title": "Wydatki",
      "expenses.empty": "Brak wydatków. Dodaj pierwszy w formularzu obok.",
      "expense.paidBy": "zapłacone przez",
      "expense.payerTitle": "Płatnik:",
      "expense.delete": "Usuń wydatek",
      "cat.other": "inne",

      "add.title": "Dodaj wydatek",
      "add.description": "Opis",
      "add.descriptionPlaceholder": "np. Hotel",
      "add.category": "Kategoria",
      "add.amount": "Kwota (PLN)",
      "add.payer": "Płatnik",
      "add.splitAria": "Sposób podziału",
      "split.equal": "Równo",
      "split.percentage": "Procenty",
      "split.exact": "Kwoty",
      "add.participants": "Uczestnicy",
      "add.shareAria": "Udział:",
      "add.submit": "Dodaj wydatek",
      "add.needMembers": "Dodaj członków do grupy, zanim dodasz wydatki.",

      "members.title": "Członkowie",
      "members.add": "Dodaj członka",
      "members.pickAria": "Osoba do dodania",

      "hint.equal": "Każda zaznaczona osoba płaci tyle samo.",
      "hint.percentage": "Wpisz procent dla każdego uczestnika. Suma musi wynosić 100.",
      "hint.exact": "Wpisz kwotę dla każdego uczestnika. Suma musi być równa kwocie wydatku.",
      "summary.perPerson": "≈ {value} PLN na osobę"
    },
    en: {
      "aria.lang": "Language",
      "aria.theme": "Theme",
      "tagline": "Settle shared expenses with the fewest transfers",

      "groups.title": "Your groups",
      "groups.lead": "Track who paid for what, split it fairly and settle up with the fewest transfers.",
      "empty.title": "No groups yet",
      "empty.text": "Add people, then create the first group below.",
      "newGroup.title": "New group",
      "newGroup.name": "Group name",
      "newGroup.placeholder": "e.g. Weekend in the mountains",
      "newGroup.members": "Members",
      "newGroup.create": "Create group",
      "newGroup.needPerson": "Add at least one person first.",
      "people.title": "People",
      "people.placeholder": "Name",
      "people.aria": "Person name",
      "people.add": "Add person",

      "group.back": "All groups",
      "group.delete": "Delete group",
      "confirm.deleteGroup": "Delete this group and all its expenses?",
      "confirm.deleteExpense": "Delete this expense?",

      "stats.total": "Total spent",
      "stats.perPerson": "Per person",
      "stats.expenses": "Expenses",
      "stats.members": "Members",

      "balances.title": "Balances",
      "balances.hint": "Right of the line: the group owes this person. Left: this person owes the group.",
      "settlement.title": "Settlement",
      "settlement.pays": "pays",
      "settlement.done": "All settled up.",

      "expenses.title": "Expenses",
      "expenses.empty": "No expenses yet. Add the first one in the form next to this.",
      "expense.paidBy": "paid by",
      "expense.payerTitle": "Paid by:",
      "expense.delete": "Delete expense",
      "cat.other": "other",

      "add.title": "Add expense",
      "add.description": "Description",
      "add.descriptionPlaceholder": "e.g. Hotel",
      "add.category": "Category",
      "add.amount": "Amount (PLN)",
      "add.payer": "Paid by",
      "add.splitAria": "Split type",
      "split.equal": "Equal",
      "split.percentage": "Percentage",
      "split.exact": "Exact",
      "add.participants": "Participants",
      "add.shareAria": "Share for",
      "add.submit": "Add expense",
      "add.needMembers": "Add members to the group before adding expenses.",

      "members.title": "Members",
      "members.add": "Add member",
      "members.pickAria": "Person to add",

      "hint.equal": "Everyone ticked pays the same amount.",
      "hint.percentage": "Enter each participant's percentage. The total must be 100.",
      "hint.exact": "Enter each participant's amount. The total must equal the expense amount.",
      "summary.perPerson": "≈ {value} PLN per person"
    }
  };

  let lang = DEFAULT_LANG;
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored && dict[stored]) {
      lang = stored;
    }
  } catch (error) { }

  const t = (key, vars) => {
    let text = (dict[lang] && dict[lang][key]) || dict.en[key] || key;
    if (vars) {
      Object.keys(vars).forEach((name) => {
        text = text.replace(`{${name}}`, vars[name]);
      });
    }
    return text;
  };
  window.t = t;
  window.getLang = () => lang;

  const knownOther = Object.keys(dict).map((code) => dict[code]["cat.other"]);

  const ATTRIBUTES = [
    ["data-i18n-placeholder", "placeholder"],
    ["data-i18n-title", "title"],
    ["data-i18n-aria", "aria-label"],
  ];

  const apply = () => {
    root.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
      element.textContent = t(element.dataset.i18n);
    });

    ATTRIBUTES.forEach(([source, target]) => {
      document.querySelectorAll(`[${source}]`).forEach((element) => {
        const suffix = element.dataset.i18nSuffix;
        const text = t(element.getAttribute(source));
        element.setAttribute(target, suffix ? `${text} ${suffix}` : text);
      });
    });

    const formatter = new Intl.DateTimeFormat(LOCALES[lang], { day: "2-digit", month: "short", year: "numeric" });
    document.querySelectorAll("time[data-date]").forEach((element) => {
      element.textContent = formatter.format(new Date(`${element.dataset.date}T00:00:00`));
    });

    document.querySelectorAll("[data-category]").forEach((element) => {
      const raw = element.dataset.category;
      element.textContent = knownOther.includes(raw) ? t("cat.other") : raw;
    });

    const categoryInput = document.querySelector('input[name="category"]');
    if (categoryInput && knownOther.includes(categoryInput.value)) {
      categoryInput.value = t("cat.other");
    }

    const switchButton = document.getElementById("lang-toggle");
    if (switchButton) {
      switchButton.setAttribute("aria-checked", String(lang === "en"));
    }

    document.dispatchEvent(new CustomEvent("langchange", { detail: { lang } }));
  };

  const setLang = (next) => {
    lang = next;
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (error) { }
    apply();
  };

  const switchButton = document.getElementById("lang-toggle");
  if (switchButton) {
    switchButton.addEventListener("click", () => setLang(lang === "pl" ? "en" : "pl"));
  }

  apply();
})();