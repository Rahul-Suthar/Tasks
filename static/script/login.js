document.addEventListener("DOMContentLoaded", () => {
    const toggler = document.querySelector(".toggler");
    const slider = document.querySelector(".slider");
    const loginBox = document.querySelector(".login-box");
    const signupBox = document.querySelector(".signup-box");
    const formSection = document.querySelector(".form-section");

    document.querySelector(".login").addEventListener("click", () => {
        slider.classList.remove("moveslider");
        formSection.classList.remove("form-section-move");
    });

    document.querySelector(".signup").addEventListener("click", () => {
        slider.classList.add("moveslider");
        formSection.classList.add("form-section-move");
    });
});
