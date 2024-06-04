const menuOpenbtn = document.querySelector(".menu-logo");
const menuClosebtn = document.querySelector(".cancel-btn-nav");
const nav_bar = document.querySelector(".nav-con-home");
// drop down //
// const select_dropContainer = document.querySelector(".gener-title-con");
// const option_drop = document.querySelector(".gener-select");
// const downArrow = document.querySelector(".down-arw");
// const upArrow = document.querySelector(".up-arw");
// const Select_title = document.querySelector(".title-final");
// const optionValueCon = option_drop.children;


let open_close_flag = false;
let select_openFlag = false;

function setValueSelect(value){
    Select_title.innerText = value
}

// for(let i =0 ;i<optionValueCon.length;i++){
//     optionValueCon[i].addEventListener("click",()=>{
//         setValueSelect(optionValueCon[i].children[0].innerText);
//         option_drop.style.display = "none";
//         select_openFlag = false;
//     })
// }


// select_dropContainer.addEventListener("click",()=>{
//     if(!select_openFlag){
//         select_openFlag = true;
//         option_drop.style.display = "block";
//         downArrow.style.transform = "rotate(-180deg)";
//         // upArrow.style.display = "block";
//     }else {
//         select_openFlag = false;
//         option_drop.style.display = "none";
//         downArrow.style.transform = "rotate(-360deg)";
//         // upArrow.style.display = "none";

//     }
// })





menuOpenbtn.addEventListener("click",()=>{
    if (!open_close_flag){ 
        nav_bar.style.right = "0%";
        open_close_flag = true;
    }
})
menuClosebtn.addEventListener("click",()=>{
    if (open_close_flag){ 
        nav_bar.style.right = "-70%";
        open_close_flag = false;
    }
})