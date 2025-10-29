document.addEventListener('DOMContentLoaded', function() {
  const dropdownBtn = document.getElementById('userDropdownBtn');
  const dropdownMenu = document.getElementById('userDropdownMenu');

  if (!dropdownBtn || !dropdownMenu) {
    return;
  }

  dropdownBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    toggleDropdown();
  });

  document.addEventListener('click', function(e) {
    const userDropdown = dropdownBtn.closest('.user-dropdown');
    
    if (userDropdown && !userDropdown.contains(e.target)) {
      closeDropdown();
    }
  });

  function toggleDropdown() {
    const isOpen = dropdownMenu.classList.contains('active');
    
    if (isOpen) {
      closeDropdown();
    } else {
      openDropdown();
    }
  }

  function openDropdown() {
    dropdownMenu.classList.add('active');
    dropdownBtn.setAttribute('aria-expanded', 'true');
  }

  function closeDropdown() {
    dropdownMenu.classList.remove('active');
    dropdownBtn.setAttribute('aria-expanded', 'false');
  }

  dropdownMenu.addEventListener('click', function(e) {
    if (e.target.closest('.dropdown-item--toggle')) {
      e.stopPropagation();
    }
  });
});