document.querySelectorAll('.tabs-wrapper').forEach((e) => {
    let tabTabs = e.querySelectorAll('.tabs .tab');
    let tabItems = e.querySelectorAll('.tabs-items .item');
    let icons = e.querySelectorAll('.tabs .tab i');
    let buttons = e.querySelectorAll('.tabs-items .item .btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            let target = btn.getAttribute('data-target');
            let tables = document.querySelectorAll('.content__features table');
            tables.forEach(table => {
                if (table.id === target) {
                    table.style.display = 'table'; 
                } else {
                    table.style.display = 'none'; 
                }
            });
        });
    });
    for(let i = 0; i < tabTabs.length; i++) {
        tabTabs[i].onclick = () => {
            if(tabTabs[i].classList.contains('on')) { 
                tabTabs[i].classList.remove('on');
                tabItems[i].classList.remove('on');
                icons[i].classList.remove('bx-chevron-up');
                icons[i].classList.add('bx-chevron-right');
            } else {
                tabTabs.forEach((e) => { e.classList.remove('on') }); 
                tabItems.forEach((e) => { e.classList.remove('on') });
                icons.forEach((e) => { e.classList.remove('bx-chevron-up') });
                icons.forEach((e) => { e.classList.add('bx-chevron-right') });
                tabTabs[i].classList.add('on');
                tabItems[i].classList.add('on');
                icons[i].classList.remove('bx-chevron-right');
                icons[i].classList.add('bx-chevron-up');
            }
        }
    }
});