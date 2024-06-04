const mobile_menuContainer = document.querySelector(".mb-menu-con");
const cancel_btn = document.querySelector(".cancel-btn-mb-menu");
const menu_btn = document.querySelector(".mb-menu");


menu_btn.addEventListener("click",()=>{
    mobile_menuContainer.style.left = "0rem";
})
cancel_btn.addEventListener("click",()=>{
    mobile_menuContainer.style.left = "-100rem";
})