  // ---------- Generic toggle helper ----------
  // fieldIds: inputs/selects that will be enabled/disabled based on toggle state
  function setupToggle(toggleId, statusTextId, fieldIds, offLabel, onLabel) {
    const toggle = document.getElementById(toggleId);
    const statusText = document.getElementById(statusTextId);
    if (!toggle || !statusText) return;
    
    toggle.addEventListener('change', () => {
      const isOn = toggle.checked;
      statusText.textContent = isOn ? onLabel : offLabel;
      fieldIds.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.disabled = !isOn;
      });
    });
  }

  setupToggle('poaToggle', 'poaStatusText',
    ['poa_first_name', 'poa_last_name', 'poa_phone_primary', 'poa_phone_secondary', 'poa_relationship'],
    'No — POA not on file', 'Yes — POA on file');
  // DNR toggle: change text color to red and bold when enabled
  const dnrToggle = document.getElementById('dnrToggle');
  const dnrStatusText = document.getElementById('dnrStatusText');
  if (dnrToggle && dnrStatusText) {
    dnrToggle.addEventListener('change', () => {
      const isOn = dnrToggle.checked;
      dnrStatusText.textContent = isOn ? 'Yes — DNR active' : 'No — DNR not active';
      dnrStatusText.classList.toggle('flag-status-critical', isOn);
    });
  }

  // ---------- Duplicate name check ----------
  const lastNameInput = document.querySelector('input[name="last_name"]');
  const firstNameInput = document.querySelector('input[name="first_name"]');
  const duplicateWarning = document.getElementById('duplicateWarning');

  if (lastNameInput && firstNameInput && duplicateWarning) {
    const checkDuplicate = async () => {
      const firstName = firstNameInput.value.trim();
      const lastName = lastNameInput.value.trim();
      if (!lastName || !firstName) {
        duplicateWarning.style.display = 'none';
        return;
      }
      try {
        const url = `/residents/check_similar/?first_name=${encodeURIComponent(firstName)}&last_name=${encodeURIComponent(lastName)}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        duplicateWarning.style.display = data.exists ? 'flex' : 'none';
      } catch (err) {
        console.warn('Duplicate check unavailable:', err);
      }
    };
    
    let debounceTimer;
    const debouncedCheck = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(checkDuplicate, 500);
    };

    lastNameInput.addEventListener('input', debouncedCheck);
    firstNameInput.addEventListener('input', debouncedCheck);
  }

  // ---------- Real-time Validation List Update ----------
  const valReq = document.getElementById('val-req');
  const valSsn = document.getElementById('val-ssn');
  const valEm = document.getElementById('val-em');

  const ssnInput = document.querySelector('input[name="ssn"]');
  const emFirst = document.querySelector('input[name="emergency_first_name"]');
  const emLast = document.querySelector('input[name="emergency_last_name"]');
  const emPhone = document.querySelector('input[name="emergency_phone_primary"]');
  const requiredInputs = document.querySelectorAll('input[required], select[required]');

  function updateValidationUI() {
    // 1. Check all required fields
    let allReqFilled = true;
    requiredInputs.forEach(el => {
      if (!el.value.trim()) allReqFilled = false;
    });
    if (valReq) {
      if (allReqFilled) valReq.classList.add('valid');
      else valReq.classList.remove('valid');
    }

    // 2. Check SSN format
    if (valSsn && ssnInput) {
      const ssnVal = ssnInput.value.trim();
      const ssnRegex = /^[\dX]{3}-[\dX]{2}-[\dX]{4}$/i;
      if (ssnVal && ssnRegex.test(ssnVal)) valSsn.classList.add('valid');
      else valSsn.classList.remove('valid');
    }

    // 3. Emergency Contact
    if (valEm && emFirst && emLast && emPhone) {
      if (emFirst.value.trim() && emLast.value.trim() && emPhone.value.trim()) {
        valEm.classList.add('valid');
      } else {
        valEm.classList.remove('valid');
      }
    }
  }

  if (valReq || valSsn || valEm) {
    document.addEventListener('input', updateValidationUI);
    updateValidationUI(); // initial run
  }

  // ---------- Inline validation on Save ----------
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', (e) => {
      let hasError = false;
      form.querySelectorAll('[required]').forEach((field) => {
        const group = field.closest('.form-group');
        const errorText = group ? group.querySelector('.error-text') : null;
        if (!field.value.trim() && !field.disabled) {
          hasError = true;
          if (group) group.classList.add('has-error');
          if (errorText) errorText.textContent = 'This field is required.';
        } else {
          if (group) group.classList.remove('has-error');
          if (errorText) errorText.textContent = '';
        }
      });
      if (hasError) {
        e.preventDefault();
        const firstError = form.querySelector('.has-error');
        if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }
