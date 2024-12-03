document.addEventListener('DOMContentLoaded', () => {
    const addCarForm = document.querySelector('form');

    if (addCarForm) {
        addCarForm.addEventListener('submit', async (e) => {
            e.preventDefault(); 
            const formData = new FormData(addCarForm);
            try {
                const response = await fetch('/add-car', {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    console.log(data.message); 
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2500); 
                } else {
                    alert(data.message || 'Failed to add the car. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});
