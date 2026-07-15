// Princeton Asset Management — shared behaviors
(function () {
  "use strict";

  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.querySelector(".mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Fade-up reveal on scroll (respects prefers-reduced-motion via CSS)
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = document.querySelectorAll(".reveal");
  if (!reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Pause hero video if reduced motion requested
  if (reduced) {
    var v = document.querySelector(".hero-media");
    if (v && v.tagName === "VIDEO") { v.removeAttribute("autoplay"); v.pause(); }
  }

  // Hover-play segment videos (desktop pointers only; posters elsewhere)
  var canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  document.querySelectorAll(".card-media video").forEach(function (v) {
    if (reduced || !canHover) { v.removeAttribute("autoplay"); return; }
    var card = v.closest("a.card") || v.parentElement;
    card.addEventListener("mouseenter", function () { v.play().catch(function () {}); });
    card.addEventListener("mouseleave", function () { v.pause(); });
    card.addEventListener("focus", function () { v.play().catch(function () {}); }, true);
    card.addEventListener("blur", function () { v.pause(); }, true);
  });

  // Lead magnet form (gated PDF download)
  document.querySelectorAll(".lead-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.querySelector('input[name="name"]');
      var email = form.querySelector('input[name="email"]');
      var honeypot = form.querySelector(".honeypot");
      var ok = true;

      form.querySelectorAll(".field-error").forEach(function (el) { el.style.display = "none"; });
      if (!name.value.trim()) {
        name.parentElement.querySelector(".field-error").style.display = "block";
        ok = false;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
        email.parentElement.querySelector(".field-error").style.display = "block";
        ok = false;
      }
      if (!ok) { (name.value.trim() ? email : name).focus(); return; }
      if (honeypot && honeypot.value) { return; } // bot

      // PRODUCTION: set data-endpoint on the form to your form service URL
      // (Formspree, ConvertKit, Squarespace form block, etc.). The download is
      // shown regardless so a service hiccup never blocks the prospect.
      var endpoint = form.getAttribute("data-endpoint");
      if (endpoint) {
        var data = new FormData(form);
        fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .catch(function () { /* non-blocking */ });
      }

      var success = form.parentElement.querySelector(".lm-success");
      form.style.display = "none";
      if (success) { success.style.display = "block"; }
    });
  });
})();
