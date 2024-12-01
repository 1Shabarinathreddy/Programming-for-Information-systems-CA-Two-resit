document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username_or_email = document.getElementById('username_or_email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username_or_email, password }),
                });

                console.log('Response status:', response.status); 
            } catch (error) {
                console.error('Error during fetch:', error); 
            }
        });
    }
});
