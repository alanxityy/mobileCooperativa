// Ativa troca de abas mesmo sem bootstrap
(function () {
  function initTabs(scope) {
    const container = scope || document;
    const tabs = container.querySelectorAll('.nav-tabs .nav-link');
    if (!tabs.length) return;

    tabs.forEach(link => {
      // evita duplo-bind
      if (link.dataset.tabsFixBound) return;
      link.dataset.tabsFixBound = "1";

      link.addEventListener('click', function (ev) {
        ev.preventDefault();
        const targetSel = this.getAttribute('href');
        if (!targetSel || !targetSel.startsWith('#')) return;

        // desativa todas
        tabs.forEach(a => a.classList.remove('active'));
        container.querySelectorAll('.tab-pane').forEach(p => {
          p.classList.remove('active', 'show');
          p.style.display = 'none';
        });

        // ativa a clicada
        this.classList.add('active');
        const pane = container.querySelector(targetSel);
        if (pane) {
          pane.style.display = '';
          pane.classList.add('active', 'show');
        }
      });
    });

    // se nenhuma ativa, ativa a primeira
    const anyActive = Array.from(tabs).some(a => a.classList.contains('active'));
    if (!anyActive && tabs[0]) tabs[0].click();
  }

  // inicializa
  document.addEventListener('DOMContentLoaded', function () {
    initTabs(document);
  });

  // se o Django trocar conteúdo via modal inline, tenta reinicializar
  document.addEventListener('click', function (e) {
    if (e.target.closest('.add-related, .change-related, .related-widget-wrapper-link')) {
      setTimeout(() => initTabs(document), 300);
    }
  });
})();
