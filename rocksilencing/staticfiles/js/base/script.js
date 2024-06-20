document.addEventListener("DOMContentLoaded",function (){
const body = document.querySelector("body")
console.log(body)
sidebar = body.querySelector(".sidebar")
        toggle = body.querySelector(".toggle")
        searchBtn = body.querySelector(".search-box")
        modeSwitch = body.querySelector(".toggle-switch")
        modeText = body.querySelector(".mode-text")

        toggle.addEventListener("click",()=>{
            sidebar.classList.toggle("close");

        })
});




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

