document.addEventListener("DOMContentLoaded", () => {
  //
  // 1) Главная страница: форма PDB → спиннер + валидация
  //
  const mainForm      = document.getElementById("pdb-form");
  const backBtn       = document.getElementById("backToTop");

  if (mainForm) {
    const formContainer = document.getElementById("form-container");
    const spinner       = document.getElementById("spinner-container");
    const pdb1Input     = document.getElementById("pdb_id1");
    const pdb2Input     = document.getElementById("pdb_id2");
    const submitBtn     = mainForm.querySelector('button[type="submit"]');
    const RE_PDB        = /^[A-Za-z0-9]{4}$/;

    // Проверка валидности PDB-кодов
    function validateForm() {
      const v1 = pdb1Input.value.trim().toUpperCase();
      const v2 = pdb2Input.value.trim().toUpperCase();
      submitBtn.disabled = !(RE_PDB.test(v1) && (v2 === "" || RE_PDB.test(v2)));
    }
    pdb1Input.addEventListener("input", validateForm);
    pdb2Input.addEventListener("input", validateForm);
    validateForm();

    // При сабмите → показываем спиннер вместо формы
    mainForm.addEventListener("submit", () => {
      if (formContainer && spinner) {
        formContainer.style.display = "none";
        spinner.style.display       = "flex";
      }
    });
  }

  //
  // 2) Страница результатов: форма мутаций → fetch → подсветка
  //
  const mutationForm = document.getElementById("mutation-form");
  if (mutationForm) {
    // Параметры формы
    const chainSelect = document.getElementById("chain-select");
    const resNumInput = document.getElementById("res-num");
    const origInput   = document.getElementById("orig-aa");
    const mutInput    = document.getElementById("mut-aa");
    const resultDiv   = document.getElementById("mutation-result");

    mutationForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      // берем PDB из глобала (вы выставляете его в result.html)
      const PDB_ID = window.PDB_ID;

      // собираем строку мутации: A25D
      const chain  = chainSelect.value;
      const resNum = resNumInput.value.trim();
      const origAA = origInput.value.trim().toUpperCase();
      const mutAA  = mutInput.value.trim().toUpperCase();
      const mutation = `${chain}${resNum}${mutAA}`;

      // ваш GET-эндпоинт
      const url = `/api/mutation_metrics/${PDB_ID}/${mutation}`;

      try {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(resp.statusText);
        const data = await resp.json();

        // Показываем текстовый результат
        resultDiv.innerHTML = `
          <p>
            Mutation: <strong>${mutation}</strong><br>
            RMSD: <strong>${data.rmsd.toFixed(3)} Å</strong><br>
            COM shift: <strong>${data.center_of_mass_diff.toFixed(3)} Å</strong>
          </p>
        `;

        // Подсветим в NGL
        if (window.stage1) {
          window.stage1.addRepresentation("ball+stick", {
            sele: `${chain} and ${resNum}`,
            colorValue: 0xFF0000,
            scale: 2.5
          });
          window.stage1.autoView();
        }
      } catch (err) {
        resultDiv.textContent = "Error: " + err.message;
        console.error(err);
      }
    });
  }

  //
  // 3) Back-to-top (универсально для всех страниц)
  //
  if (backBtn) {
    window.addEventListener("scroll", () => {
      backBtn.style.display = window.scrollY > 200 ? "block" : "none";
    });
    backBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});
