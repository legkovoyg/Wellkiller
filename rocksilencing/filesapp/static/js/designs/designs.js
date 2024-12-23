document.addEventListener('DOMContentLoaded', function() {
   // DOM элементы
   const modalOverlay = document.querySelector('.modal-overlay');
   const createDesignTriggers = document.querySelectorAll('.create-design-trigger');
   const modalClose = document.querySelector('.modal-close');
   const modalCancel = document.querySelector('.modal-btn.cancel');
   const createButton = document.querySelector('.modal-btn.create');
   
   // Элементы формы
   const designNameInput = document.getElementById('design-name');
   const fieldInput = document.getElementById('field-custom-input');
   const clusterInput = document.getElementById('cluster-custom-input');
   const wellInput = document.getElementById('well-custom-input');
   const calcTypeSelect = document.getElementById('calc-type');

   function openModal() {
       modalOverlay.style.display = 'block';
       designNameInput.value = '';
       fieldInput.value = '';
       clusterInput.value = '';
       wellInput.value = '';
   }

   function closeModal() {
       modalOverlay.style.display = 'none';
   }

   function getCookie(name) {
       let cookieValue = null;
       if (document.cookie && document.cookie !== '') {
           const cookies = document.cookie.split(';');
           for (let i = 0; i < cookies.length; i++) {
               const cookie = cookies[i].trim();
               if (cookie.substring(0, name.length + 1) === (name + '=')) {
                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
               }
           }
       }
       return cookieValue;
   }

   createButton.addEventListener('click', function() {
       const designName = designNameInput.value.trim();
       if (!designName) {
           alert("Введите название дизайна!");
           return;
       }

       const payload = {
           name: designName,
           field: fieldInput.value.trim() || null,
           cluster: clusterInput.value.trim() || null,
           well: wellInput.value.trim() || null,
           calc_type: calcTypeSelect.value
       };

       fetch('/files/ajax_create_design/', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
               'X-CSRFToken': getCookie('csrftoken')
           },
           body: JSON.stringify(payload)
       })
       .then(response => response.json())
       .then(data => {
           if (data.status === 'ok') {
               alert('Дизайн успешно создан!');
               closeModal();
               window.location.reload();
           } else {
               alert('Ошибка при создании дизайна: ' + data.message);
           }
       })
       .catch(err => {
           console.error('Ошибка:', err);
           alert('Произошла ошибка при создании дизайна');
       });
   });

   createDesignTriggers.forEach(trigger => {
       trigger.addEventListener('click', (e) => {
           e.preventDefault();
           openModal();
       });
   });

   if (modalClose) modalClose.addEventListener('click', closeModal);
   if (modalCancel) modalCancel.addEventListener('click', closeModal);

   if (modalOverlay) {
       modalOverlay.addEventListener('click', (e) => {
           if (e.target === modalOverlay) {
               closeModal();
           }
       });
   }

   const tableRows = document.querySelectorAll('.history-table tbody tr');
   tableRows.forEach(row => {
       row.addEventListener('click', function() {
           const calcType = this.querySelector('td:nth-child(2)').textContent;
           const url = window.CALCULATOR_URLS[calcType];
           if (url) {
               window.location.href = url;
           }
       });
   });

   fieldInput.style.display = 'block';
   clusterInput.style.display = 'block';
   wellInput.style.display = 'block';
});