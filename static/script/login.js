const slider = document.querySelector(".slider");
const formSection = document.querySelector(".form-section");
const loginBtn = document.querySelector(".login");
const signupBtn = document.querySelector(".signup");

// Toggle functionality
loginBtn.addEventListener("click", () => {
    slider.classList.remove("moveslider");
    formSection.classList.remove("form-section-move");
});

signupBtn.addEventListener("click", () => {
    slider.classList.add("moveslider");
    formSection.classList.add("form-section-move");
});
