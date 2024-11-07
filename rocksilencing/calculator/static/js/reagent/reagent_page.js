document.querySelectorAll('.tabs-wrapper').forEach((e)=>{
    let tabs = e.querySelectorAll('.tab');
    let innerTabs = e.querySelectorAll('.inner-tabs');
    let innerTab = e.querySelectorAll('.inner-tabs span');
    let btn = e.querySelectorAll('.tabs-items');
    let bxSalt = e.querySelectorAll('.inner-tab-salt i');
    let icons = e.querySelectorAll('.tabs i');
    let buttons = e.querySelectorAll('.btn');
    for(let i = 0; i < tabs.length; i++) {
        tabs[i].onclick = () => {
            if(tabs[i].classList.contains('on')) { 
                tabs[i].classList.remove('on');
                innerTabs[i].classList.remove('on')
                icons[i].classList.remove('bx-chevron-down');
                icons[i].classList.add('bx-chevron-right');
            } else {
                tabs[i].classList.add('on');
                innerTabs[i].classList.add('on')
                icons[i].classList.remove('bx-chevron-right');
                icons[i].classList.add('bx-chevron-down');
            
            }
        }
    }

    for(let i = 0; i <  innerTab.length; i++) {
        innerTab[i].onclick = () => {
            if(innerTab[i].classList.contains('on')) { 
                innerTab[i].classList.remove('on');
                btn[i].classList.remove('on');
                bxSalt[i].classList.remove('bx-chevron-down');
                bxSalt[i].classList.add('bx-chevron-right');
            } else {
                innerTab[i].classList.add('on');
                btn[i].classList.add('on');
                bxSalt[i].classList.remove('bx-chevron-right');
                bxSalt[i].classList.add('bx-chevron-down');
            }
        }
    }
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            let target = btn.getAttribute('data-target');
            let tables = document.querySelectorAll('.content__features table');
            let salts = document.querySelectorAll('.content__table table tr:not(:first-child)')
            let header = document.querySelector('.content__features')
            console.log(header)
            console.log(header)
            tables.forEach(table => {
                if (table.id === target) {
                    table.style.display = 'table';
                } else {
                    table.style.display = 'none'; 
                }
            })
            salts.forEach(salt => {
                if (salt.id === target) {
                    salt.style.display = 'table-row';
                } else {
                    salt.style.display = 'none';
                }
            });
            if (header.style.display == 'none'){
            header.style.display = 'block';}
    })});
})