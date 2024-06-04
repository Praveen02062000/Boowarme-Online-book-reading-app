const eye_containerLib = document.querySelector(".eye-con-lib");
const eyenotOpen = document.querySelector(".notopen");
const eyeOpen = document.querySelector(".open");
const passwordField = document.querySelector('.pass');

var PasswordFlag = false;
eyeOpen.style.display = "none";


eye_containerLib.addEventListener("click",()=>{
    if(!PasswordFlag) {
        eyeOpen.style.display = "block";
        eyenotOpen.style.display = "none";
        passwordField.type = "text";
        PasswordFlag = true;
    }else {
        eyeOpen.style.display = "none";
        eyenotOpen.style.display = "block";
        passwordField.type = "password";
        PasswordFlag = false;
    }
})

