// Tap-through lead form. Without JavaScript every step shows at once and the
// form posts straight to FormSubmit, which redirects to thanks.html (_next).
(function () {
  var form = document.getElementById('lead-form');
  if (!form) return;

  var steps = Array.prototype.slice.call(form.querySelectorAll('.step'));
  var count = form.querySelector('.lead-count');
  var bar = form.querySelector('.lead-bar span');
  var back = form.querySelector('.back');
  var status = form.querySelector('.lead-status');
  var send = form.querySelector('button[type="submit"]');
  var townSelect = form.querySelector('#lead-town');
  var townOther = form.querySelector('#lead-town-other');
  var townErr = form.querySelector('#town-err');
  var leadErr = form.querySelector('#lead-err');
  var townNext = form.querySelector('.step-town .next');
  var locOther = form.querySelector('#lead-location-other');
  var locErr = form.querySelector('#location-err');
  var locNext = form.querySelector('.step-location .next');
  var sizeInput = form.querySelector('#lead-size');
  var current = 0;
  var pending = null;
  var arrowed = false;
  var townKeyed = false;

  form.classList.add('js');
  form.noValidate = true;
  if (back) back.hidden = false;

  function value(name) {
    var el = form.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : '';
  }

  // The water heater steps (type, venting, location) don't apply to boiler or general plumbing requests.
  function skipped(step) {
    return step.getAttribute('data-skip-unless-heater') !== null &&
      value('Issue') === 'Boiler or other plumbing';
  }

  function visibleSteps() {
    return steps.filter(function (s) { return !skipped(s); });
  }

  function show(i, focus) {
    current = i;
    steps.forEach(function (s, n) { s.hidden = n !== i; });
    var vis = visibleSteps();
    var pos = vis.indexOf(steps[i]) + 1;
    if (count) count.textContent = 'Step ' + pos + ' of ' + vis.length;
    if (bar) bar.style.width = (pos / vis.length * 100) + '%';
    if (back) back.style.visibility = i === 0 ? 'hidden' : 'visible';
    if (focus) {
      var legend = steps[i].querySelector('legend');
      if (legend) { legend.setAttribute('tabindex', '-1'); legend.focus({ preventScroll: true }); }
      var rect = form.getBoundingClientRect();
      if (rect.top < 64) window.scrollTo({ top: rect.top + window.pageYOffset - 84 });
    }
  }

  function next() {
    var i = current + 1;
    while (i < steps.length && skipped(steps[i])) i++;
    if (i < steps.length) show(i, true);
  }

  function prev() {
    var i = current - 1;
    while (i > 0 && skipped(steps[i])) i--;
    if (i >= 0) show(i, true);
  }

  // One advance per step: a double-tap can't skip a question.
  function advanceSoon(delay) {
    if (pending) return;
    var from = current;
    pending = setTimeout(function () {
      pending = null;
      if (current === from) next();
    }, delay);
  }

  var otherField = townOther.closest('.field');
  function syncTown() {
    var other = townSelect.value === 'Other';
    otherField.hidden = !other;
    townOther.required = other;
  }

  var locField = locOther.closest('.field');
  function syncLocation() {
    var other = value('Water heater location') === 'Other';
    locField.hidden = !other;
    if (!other) { locErr.textContent = ''; locOther.removeAttribute('aria-invalid'); }
  }

  function fieldError(el, msg, input) {
    el.textContent = msg;
    if (input) {
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', el.id);
    }
  }

  // Tapping an answer moves on. Arrow keys only change the selection, so
  // keyboard users can look through the options; Enter or Next continues.
  form.addEventListener('keydown', function (e) {
    var t = e.target;
    if (t.type === 'radio') {
      if (e.key.indexOf('Arrow') === 0) {
        arrowed = true;
        setTimeout(function () { arrowed = false; }, 80);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        // Go through the step's Next button so its checks run.
        if (form.querySelector('input[name="' + t.name + '"]:checked')) t.closest('.step').querySelector('.next').click();
      }
    } else if (t === townSelect) {
      townKeyed = true;
    }
  });
  townSelect.addEventListener('pointerdown', function () { townKeyed = false; });

  form.addEventListener('click', function (e) {
    var t = e.target;
    if (t.type !== 'radio' || arrowed) return;
    if (t.closest('.step') !== steps[current]) return;
    // "Other" location opens a text box instead of moving on.
    if (t.name === 'Water heater location' && t.value === 'Other') return;
    advanceSoon(160);
  });

  form.addEventListener('change', function (e) {
    var t = e.target;
    if (t.type === 'radio') {
      var nb = t.closest('.step').querySelector('.next');
      if (nb) nb.hidden = false;
      if (t.name === 'Water heater location') {
        syncLocation();
        if (t.value === 'Other') locOther.focus();
      }
    } else if (t === townSelect) {
      syncTown();
      townErr.textContent = '';
      townSelect.removeAttribute('aria-invalid');
      if (townSelect.value === 'Other') townOther.focus();
      else if (townSelect.value && !townKeyed) advanceSoon(120);
    }
  });

  Array.prototype.forEach.call(form.querySelectorAll('.step .next'), function (btn) {
    if (btn === townNext || btn === locNext) return;
    btn.addEventListener('click', next);
  });

  townNext.addEventListener('click', function () {
    townSelect.removeAttribute('aria-invalid');
    townOther.removeAttribute('aria-invalid');
    townErr.textContent = '';
    if (!townSelect.value) {
      fieldError(townErr, 'Choose your town.', townSelect);
      townSelect.focus();
      return;
    }
    if (townSelect.value === 'Other' && !townOther.value.trim()) {
      fieldError(townErr, 'Type your town.', townOther);
      townOther.focus();
      return;
    }
    next();
  });
  townOther.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); townNext.click(); }
  });
  locNext.addEventListener('click', function () {
    locErr.textContent = '';
    locOther.removeAttribute('aria-invalid');
    if (value('Water heater location') === 'Other' && !locOther.value.trim()) {
      fieldError(locErr, 'Tell us where the water heater is.', locOther);
      locOther.focus();
      return;
    }
    next();
  });
  [locOther, sizeInput].forEach(function (el) {
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); el.closest('.step').querySelector('.next').click(); }
    });
  });
  if (back) back.addEventListener('click', prev);

  function fail(msg) {
    status.className = 'lead-status err';
    status.innerHTML = msg;
    status.scrollIntoView({ block: 'nearest' });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.querySelector('input[name="_honey"]').value) return;

    var name = form.querySelector('#lead-name');
    var phone = form.querySelector('#lead-phone');
    var firstBad = null;
    [name, phone].forEach(function (el) {
      var bad = !el.value.trim() || (el === phone && el.value.replace(/\D/g, '').length < 10);
      el.setAttribute('aria-invalid', bad ? 'true' : 'false');
      if (bad && !firstBad) firstBad = el;
    });
    if (firstBad) {
      fieldError(leadErr, 'Add your name and a phone number we can call back.');
      name.setAttribute('aria-describedby', 'lead-err');
      phone.setAttribute('aria-describedby', 'lead-err');
      firstBad.focus();
      return;
    }
    leadErr.textContent = '';

    var town = townSelect.value === 'Other' ? (townOther.value.trim() || 'Other') : townSelect.value;
    var boiler = value('Issue') === 'Boiler or other plumbing';
    var loc = value('Water heater location');
    if (loc === 'Other') loc = 'Other: ' + (locOther.value.trim() || 'not given');
    var data = {
      'Issue': value('Issue'),
      'Heater type': boiler ? 'n/a' : (value('Heater type') || 'not answered')
    };
    // Venting and location only go out for water heater requests.
    if (!boiler) {
      data['Water heater venting'] = value('Water heater venting') || 'not answered';
      data['Water heater location'] = loc || 'not answered';
    }
    Object.assign(data, {
      'Equipment size': sizeInput.value.trim() || 'not provided',
      'How soon': value('How soon'),
      'Town': town,
      'Name': name.value.trim(),
      'Phone': phone.value.trim(),
      'Note': form.querySelector('#lead-note').value.trim()
    });
    form.querySelectorAll('input[type="hidden"]').forEach(function (h) {
      if (h.name !== '_next') data[h.name] = h.value;
    });

    var thanks = new URL('thanks.html', window.location.href).href;
    if (window.HWT_PREVIEW) { window.HWT_PREVIEW(data); return; }

    send.disabled = true;
    send.textContent = 'Sending…';
    status.className = 'lead-status';
    status.textContent = '';

    fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); })
      .then(function (res) {
        if (!res.ok || String(res.body.success) !== 'true') throw new Error(res.body.message || 'Send failed');
        window.location.href = thanks;
      })
      .catch(function () {
        send.disabled = false;
        send.textContent = 'Send request';
        fail('That didn’t go through. Please call <a href="tel:+17812043247">(781) 204-3247</a>.');
      });
  });

  // Browsers can restore a picked town after Back/Forward.
  syncTown();
  syncLocation();
  window.addEventListener('pageshow', function () { syncTown(); syncLocation(); });
  show(0, false);
})();
