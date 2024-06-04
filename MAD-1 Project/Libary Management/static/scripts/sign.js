const password = document.querySelector(".pass-sign");
const passwordopen = document.querySelector(".sign-open");
const passwordclose = document.querySelector(".sign-notopen");
const repassword = document.querySelector(".repass-sign");
const repasswordopen = document.querySelector(".sign-open-re");
const repasswordclose = document.querySelector(".sign-notopen-re");
const eye_container = document.querySelector(".eye-con");
const eye_btn_pass = document.querySelector("#eye-con-sign-pass");
const eye_btn_repass = document.querySelector("#eye-con-sign-repass")



let password_flag = false;
let repassword_flag = false;

passwordopen.style.display = "none";
repasswordopen.style.display = "none";


function eye_close1(){
    if (!password_flag){
        passwordopen.style.display = "block";
        passwordclose.style.display = "none";
        password_flag = true;
        password.type = "text";
    }else{
        passwordopen.style.display = "none";
        passwordclose.style.display= "block";
        password_flag = false;
        password.type = "password";
    }
}
function eye_close2(){
    if (!repassword_flag){
        repasswordopen.style.display = "block";
        repasswordclose.style.display = "none";
        repassword_flag = true;
        repassword.type = "text";
    }else{
        repasswordopen.style.display = "none";
        repasswordclose.style.display= "block";
        repassword_flag = false;
        repassword.type = "password";
    }
}



eye_btn_pass.addEventListener("click",()=>{eye_close1()})
eye_btn_repass.addEventListener("click",()=>{eye_close2()})