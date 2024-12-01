document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loadingIndicator = document.getElementById('loadingIndicator'); 

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username_or_email = document.getElementById('username_or_email').value;
            const password = document.getElementById('password').value;

            // Show loading indicator
            if (loadingIndicator) {
                loadingIndicator.style.display = 'block';
            }

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username_or_email, password }),
                });

                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error during fetch:', error);
                alert('An error occurred. Please try again.');
            } finally {
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }
            }
        });
    }
});
