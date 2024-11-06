const loginBtn = document.querySelector('.login');
const signupBtn = document.querySelector('.signup');
const slider = document.querySelector('.slider');
const formSection = document.querySelector('.form-section');

loginBtn.addEventListener('click', () => {
    slider.classList.remove('moveslider');  // Reset slider position
    formSection.classList.remove('form-section-move'); // Show login form
});

signupBtn.addEventListener('click', () => {
    slider.classList.add('moveslider'); // Move slider to signup
    formSection.classList.add('form-section-move'); // Show signup form
});
