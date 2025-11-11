document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  const isAdvancedUpload = (() => {
    const div = document.createElement('div');
    return (
      ('draggable' in div || ('ondragstart' in div && 'ondrop' in div)) &&
      'FormData' in window &&
      'FileReader' in window
    );
  })();

  const forms = document.querySelectorAll('.dropbox');
  if (!forms.length) return;

  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
  const maxSize = 5 * 1024 * 1024;

  forms.forEach(form => {
    const input = form.querySelector('input[type="file"]');
    const filenameSpan = form.querySelector('.dropbox__filename');

    const showFiles = files => {
      filenameSpan.textContent = files[0]?.name || 'Ningún archivo seleccionado';
    };

    const setError = msg => {
      form.classList.add('is-error');
      filenameSpan.textContent = msg;
      setTimeout(() => {
        form.classList.remove('is-error');
        filenameSpan.textContent = 'Ningún archivo seleccionado';
      }, 3000);
    };

    // --- Drag & Drop ---
    if (isAdvancedUpload) {
      form.classList.add('has-advanced-upload');

      const stop = e => {
        e.preventDefault();
        e.stopPropagation();
      };

      ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop']
        .forEach(evt => form.addEventListener(evt, stop));

      ['dragover', 'dragenter'].forEach(evt =>
        form.addEventListener(evt, () => form.classList.add('is-dragover'))
      );

      ['dragleave', 'dragend', 'drop'].forEach(evt =>
        form.addEventListener(evt, () => form.classList.remove('is-dragover'))
      );

      form.addEventListener('drop', e => {
        const [file] = e.dataTransfer.files || [];
        if (!file) return;

        if (!validTypes.includes(file.type)) {
          return setError('Solo imágenes: JPG, PNG, GIF, WEBP');
        }

        if (file.size > maxSize) {
          return setError('Máximo 5MB');
        }

        try {
          input.files = e.dataTransfer.files;
        } catch {
          const dt = new DataTransfer();
          dt.items.add(file);
          input.files = dt.files;
        }

        showFiles([file]);
      });
    }

    input.addEventListener('change', () => {
      if (input.files.length) showFiles(input.files);
    });
  });
});
