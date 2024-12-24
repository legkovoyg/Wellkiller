document.addEventListener('DOMContentLoaded', function() {
   const modalOverlay = document.querySelector('.modal-overlay');
   const createDesignTriggers = document.querySelectorAll('.create-design-trigger');
   const modalClose = document.querySelector('.modal-close');
   const modalCancel = document.querySelector('.modal-btn.cancel');
   const createButton = document.querySelector('.modal-btn.create');
   
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
       calcTypeSelect.value = 'Глушение скважины';
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

   // Удаление дизайна
   document.querySelectorAll('.delete-design-btn').forEach(button => {
       button.addEventListener('click', function() {
           if (confirm('Вы уверены, что хотите удалить этот дизайн?')) {
               const designId = this.dataset.uuid;
               
               fetch(`/files/delete_design/${designId}/`, {
                   method: 'POST',
                   headers: {
                       'X-CSRFToken': getCookie('csrftoken')
                   }
               })
               .then(response => response.json())
               .then(data => {
                   if (data.status === 'ok') {
                       this.closest('tr').remove();
                   } else {
                       alert('Ошибка при удалении дизайна');
                   }
               })
               .catch(error => {
                   console.error('Error:', error);
                   alert('Произошла ошибка при удалении дизайна');
               });
           }
       });
   });

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
               const createdDesignId = data.design_id;
               const baseUrl = window.CALCULATOR_URLS[payload.calc_type];
               if (baseUrl) {
                   const fullUrl = baseUrl + "?design_id=" + createdDesignId;
                   window.location.href = fullUrl;
               } else {
                   window.location.reload();
               }
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

   const moduleLinks = document.querySelectorAll('.open-module-link');
   moduleLinks.forEach(link => {
       link.addEventListener('click', async function(e) {
           e.preventDefault();

           const calcType = this.dataset.calcType;
           const designId = this.dataset.designId;

           if (!calcType || !designId) {
               return;
           }

           try {
               // Обновляем сессию перед переходом
               const response = await fetch(`/files/get_design/${designId}/`, {
                   method: 'GET',
                   headers: {
                       'X-CSRFToken': getCookie('csrftoken')
                   }
               });

               if (!response.ok) {
                   throw new Error('Ошибка получения данных дизайна');
               }

               const baseUrl = window.CALCULATOR_URLS[calcType];
               if (baseUrl) {
                   window.location.href = baseUrl + "?design_id=" + designId;
               }
           } catch (error) {
               console.error('Ошибка:', error);
               alert('Произошла ошибка при загрузке дизайна');
           }
       });
   });

   fieldInput.style.display = 'block';
   clusterInput.style.display = 'block';
   wellInput.style.display = 'block';
});