document.addEventListener('DOMContentLoaded', () => {
    const signupButton = document.getElementById('signupButton');
    if (signupButton) {
        signupButton.addEventListener('click', () => {
            window.location.href = '/signup';
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const signupButton = document.getElementById('loginButton');
    if (signupButton) {
        signupButton.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }
});