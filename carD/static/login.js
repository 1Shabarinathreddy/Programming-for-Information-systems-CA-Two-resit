document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Capture input values
            const username_or_email = document.getElementById('username_or_email').value;
            const password = document.getElementById('password').value;

            // Debugging logs to verify inputs
            console.log('Username/Email:', username_or_email);
            console.log('Password:', password);
        });
    }
});
