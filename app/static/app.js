(() => {
  const root = document.documentElement;
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const hueFromName = (name) => {
    let hue = 0;
    for (const character of name) {
      hue = (hue * 31 + character.charCodeAt(0)) % 360;
    }
    return hue;
  };

  const paintAvatars = () => {
    document.querySelectorAll("[data-avatar]").forEach((element) => {
      element.style.setProperty("--hue", hueFromName(element.dataset.avatar.trim()));
    });
  };

  const initThemeToggle = () => {
    const button = document.getElementById("theme-toggle");
    if (!button) {
      return;
    }
    const sync = () => {
      button.setAttribute("aria-checked", String((root.dataset.theme || "dark") === "light"));
    };
    button.addEventListener("click", () => {
      const next = (root.dataset.theme || "dark") === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      sync();
      try {
        localStorage.setItem("zerotab-theme", next);
      } catch (error) {
        return;
      }
    });
    sync();
  };

  const initReveal = () => {
    const items = document.querySelectorAll(".reveal");
    items.forEach((item, index) => {
      item.style.setProperty("--delay", `${Math.min(index * 70, 420)}ms`);
    });
    if (!("IntersectionObserver" in window)) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08 },
    );
    items.forEach((item) => observer.observe(item));
  };

  const easeOutCubic = (progress) => 1 - Math.pow(1 - progress, 3);

  const animateMoney = (element) => {
    const finalText = element.textContent.trim();
    const target = parseFloat(finalText);
    if (Number.isNaN(target)) {
      return;
    }
    const suffix = finalText.replace(/^-?[\d.]+/, "");
    const duration = 900;
    const startedAt = performance.now();
    const tick = (now) => {
      const progress = Math.min((now - startedAt) / duration, 1);
      element.textContent = `${(target * easeOutCubic(progress)).toFixed(2)}${suffix}`;
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        element.textContent = finalText;
      }
    };
    requestAnimationFrame(tick);
  };

  const initMoneyCounters = () => {
    if (prefersReducedMotion) {
      return;
    }
    document.querySelectorAll("[data-money]").forEach(animateMoney);
  };

  const initBalanceBars = () => {
    const rows = [...document.querySelectorAll(".balance-row")];
    if (rows.length === 0) {
      return;
    }
    const amounts = rows.map((row) => Math.abs(parseFloat(row.dataset.amount)));
    const maxAmount = Math.max(...amounts);
    setTimeout(() => {
      rows.forEach((row, index) => {
        const share = maxAmount === 0 ? 0 : amounts[index] / maxAmount;
        row.querySelector(".bar-fill").style.setProperty("--w", `${Math.round(share * 100)}%`);
      });
    }, 250);
  };

  const dismissAlert = (alert) => {
    alert.classList.add("is-leaving");
    setTimeout(() => alert.remove(), 300);
  };

  document.addEventListener("click", (event) => {
    const closeButton = event.target.closest(".alert-close");
    if (closeButton) {
      dismissAlert(closeButton.closest(".alert"));
    }
  });

  paintAvatars();
  initThemeToggle();
  initReveal();
  initMoneyCounters();
  initBalanceBars();
})();