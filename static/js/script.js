document.addEventListener("DOMContentLoaded", () => {
  // 1) Spinner & validation on main form
  const mainForm = document.getElementById("pdb-form");
  if (mainForm) {
    const formContainer = document.getElementById("form-container");
    const spinner       = document.getElementById("spinner-container");
    const pdb1Input     = document.getElementById("pdb_id1");
    const pdb2Input     = document.getElementById("pdb_id2");
    const submitBtn     = mainForm.querySelector('button[type="submit"]');
    const RE_PDB        = /^[A-Za-z0-9]{4}$/;

    function validateForm() {
      const v1 = pdb1Input.value.trim().toUpperCase();
      const v2 = pdb2Input.value.trim().toUpperCase();
      submitBtn.disabled = !(RE_PDB.test(v1) && (v2 === "" || RE_PDB.test(v2)));
    }
    pdb1Input.addEventListener("input", validateForm);
    pdb2Input.addEventListener("input", validateForm);
    validateForm();

    mainForm.addEventListener("submit", () => {
      formContainer.style.display = "none";
      spinner.style.display       = "flex";
    });
  }

  // 2) Mutation forms
  [1, 2].forEach(i => {
    const form = document.getElementById(`mutation-form-${i}`);
    if (!form) return;

    const pdbId       = form.dataset.pdb;
    const chainSelect = form.querySelector(`#chain-select-${i}`);
    const resNumInput = form.querySelector(`#res-num-${i}`);
    const origInput   = form.querySelector(`#orig-aa-${i}`);
    const mutInput    = form.querySelector(`#mut-aa-${i}`);
    const resultDiv   = document.getElementById(`mutation-result-${i}`);
    const AA_RE       = /^[A-Za-z]$/;

    form.addEventListener("submit", async e => {
      e.preventDefault();
      const chain  = chainSelect.value;
      const resNum = resNumInput.value.trim();
      const origAA = origInput.value.trim().toUpperCase();
      const mutAA  = mutInput.value.trim().toUpperCase();
      if (!AA_RE.test(origAA) || !AA_RE.test(mutAA)) {
        resultDiv.textContent = "Amino acids must be single letters";
        return;
      }

      const mutation = `${chain}${resNum}${mutAA}`;
      const url      = `/api/mutation_metrics/${pdbId}/${mutation}`;
      resultDiv.textContent = "Analyzing mutation…";

      try {
        const resp    = await fetch(url);
        const payload = await resp.json();
        if (!resp.ok) throw new Error(payload.error || resp.statusText);

        resultDiv.innerHTML = `
          <p>
            Mutation: <strong>${mutation}</strong><br>
            RMSD: <strong>${payload.rmsd.toFixed(3)} Å</strong><br>
            COM shift: <strong>${payload.center_of_mass_diff.toFixed(3)} Å</strong>
          </p>
        `;

        const comp  = i === 1 ? window.comp1 : window.comp2;
        const stage = i === 1 ? window.stage1 : window.stage2;
        if (comp) {
          comp.addRepresentation("ball+stick", {
            sele: `${resNum} and :${chain}`,
            colorValue: 0xFF0000,
            scale: 2.5
          });
          stage.autoView();
        }
      } catch (err) {
        resultDiv.textContent = "Error: " + err.message;
        console.error(err);
      }
    });
  });

  // 3) Back-to-top
  const backBtn = document.getElementById("backToTop");
  if (backBtn) {
    window.addEventListener("scroll", () => {
      backBtn.style.display = window.scrollY > 200 ? "block" : "none";
    });
    backBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});
