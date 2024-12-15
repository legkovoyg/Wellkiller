document.addEventListener("DOMContentLoaded",function (){
const body = document.querySelector("body")
// console.log(body)
sidebar = body.querySelector(".sidebar")
        toggle = body.querySelector(".toggle")
        searchBtn = body.querySelector(".search-box")
        modeSwitch = body.querySelector(".toggle-switch")
        modeText = body.querySelector(".mode-text")

        toggle.addEventListener("click",()=>{
            sidebar.classList.toggle("close");

        })
});

function mobile () {
        let newToggle = document.querySelector('.toggle-sidebar-img')
        const mainHeaderRight = document.querySelector('.main-Header__rightContent')
        const logInButton = document.querySelector('.rightContent-fourth')
        if (document.documentElement.clientWidth <= 500) {
                logInButton.style.display = 'none';
                if(!newToggle) {
                        
                        newToggle = document.createElement('img')
                        newToggle.classList.add('toggle-sidebar-img')
                        mainHeaderRight.append(newToggle)
                        newToggle.src = '/static/images/base/Frame-15003.svg'
                        newToggle.addEventListener("click",() => {
                                sidebar.classList.toggle("close");
                        })

                        hasElementsBeenAdded = true;
                }       
        
        } else {
                if (newToggle) {
                        newToggle.remove()
                        hasElementsBeenAdded = false;
                }
                logInButton.style.display = 'flex'
        }       
}
window.addEventListener('resize', mobile);
window.addEventListener('load', mobile);

        // смена темы

        // modeSwitch.addEventListener("click",()=>{
        //     body.classList.toggle("dark");
            
        //     if(body.classList.contains("dark")){
        //         modeText.innerText = "Light Mode"
        //     }
        //     else{
        //         modeText.innerText = "Dark Mode"
        //     }
            
        // })

