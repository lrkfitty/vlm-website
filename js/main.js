/* ── NAV ─────────────────────────────────────────────────────────────────── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

/* ── REVEAL ──────────────────────────────────────────────────────────────── */
const revealEls = document.querySelectorAll('.reveal-up,.reveal-left,.reveal-right,.reveal-scale');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('revealed'); revealObs.unobserve(e.target); } });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
revealEls.forEach(el => revealObs.observe(el));

window.addEventListener('load', () => {
  document.querySelectorAll('.hero .reveal-up, .hero .reveal-left').forEach((el, i) => {
    setTimeout(() => el.classList.add('revealed'), 200 + i * 100);
  });
});

/* ── LEAD FORM (CTA) ─────────────────────────────────────────────────────── */
const ctaForm    = document.getElementById('ctaForm');
const ctaSuccess = document.getElementById('ctaSuccess');

if (ctaForm) {
  ctaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn     = ctaForm.querySelector('.cta-submit');
    const btnText = btn.querySelector('.btn-text');
    const btnLoad = btn.querySelector('.btn-loading');
    btnText.style.display = 'none';
    btnLoad.style.display = 'inline';
    btn.disabled = true;

    const data = {
      name:    ctaForm.name.value.trim(),
      email:   ctaForm.email.value.trim(),
      company: ctaForm.company.value.trim(),
      source:  'vlmcreateflow.com',
    };

    try {
      const res = await fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error();
    } catch {
      // fallback — show success regardless
    }

    ctaForm.style.display    = 'none';
    ctaSuccess.style.display = 'block';
  });
}

/* ── SMOOTH SCROLL ───────────────────────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); window.scrollTo({ top: t.offsetTop - nav.offsetHeight - 20, behavior: 'smooth' }); }
  });
});
