const mobile_menuContainer = document.querySelector(".mb-menu-con");
const cancel_btn = document.querySelector(".cancel-btn-mb-menu");
const menu_btn = document.querySelector(".mb-menu");
const ADDSECTION = document.querySelector(".add-section");
const AddMainCon = document.querySelector(".add-section-pop");
const sectionCancel = document.querySelector(".cancel-logo");
const donesecBtn = document.querySelector(".sec-btn");
const main = document.querySelector(".section-body");
const section_id_setter = document.querySelector(".sec-id-seter");
const section_id_setter2 = document.querySelector(".sec-id-setter");
const sectionedit = document.querySelector(".section-edit-con");
const buttoncon = document.querySelector(".edit-btn-con");
const sectioneditcon = document.querySelector(".edit-con");
const deletecon = document.querySelector(".delete-sec");
const sectioneditcancel = document.querySelector(".edit-con-logo");
const deleteaction = document.querySelector(".delete-sec");
const applysec = document.querySelector(".apply-sec");
const OldSrcCon = document.querySelector(".old_src");
const DenyBtn = document.querySelector(".close-cancel");





let section_ID = "";

for (let i=0;i<main.children.length-1;i++){
    var div = main.children[i].children[0].children[0]
    div.addEventListener("click",(e)=>{
        section_ID = e.srcElement.attributes.data.nodeValue
        section_id_setter.value = section_ID
        section_id_setter2.value = section_ID
        sectionedit.style.display = "flex"
        old_path = main.children[i].children[1].attributes.src.nodeValue.split("/")
        finalImgname = old_path[old_path.length-1]
        OldSrcCon.value = finalImgname
        
    })   
}


buttoncon.children[0].addEventListener("click",()=>{
    buttoncon.children[0].style.borderBottom = "2px solid purple";
    buttoncon.children[1].style.borderBottom = "none";
    sectioneditcon.style.display = "block";
    deletecon.style.display = "none";
})
buttoncon.children[1].addEventListener("click",()=>{
    buttoncon.children[1].style.borderBottom = "2px solid purple";
    buttoncon.children[0].style.borderBottom = "none";
    sectioneditcon.style.display = "none";
    deletecon.style.display = "flex";
})
function close(){
    sectionedit.style.display = "none"
}
sectioneditcancel.addEventListener("click",()=>{
    close()
})
applysec.addEventListener("click",()=>{
    close()
})
DenyBtn.addEventListener("click",(e)=>{
    e.preventDefault()
    close()
})






ADDSECTION.addEventListener("click",()=>{
    AddMainCon.style.display = "flex"
})
sectionCancel.addEventListener("click",()=>{
    AddMainCon.style.display = "none"
})

donesecBtn.addEventListener("click",()=>{
    setTimeout(()=>{
        window.onload()

    },2000)
})


menu_btn.addEventListener("click",()=>{
    mobile_menuContainer.style.left = "0rem";
})
cancel_btn.addEventListener("click",()=>{
    mobile_menuContainer.style.left = "-100rem";
})