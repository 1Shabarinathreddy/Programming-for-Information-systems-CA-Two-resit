document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/my-cars');
        if (response.ok) {
            const data = await response.json();
            const carsContainer = document.getElementById('carsContainer');
            
            if (data.cars.length > 0) {
                data.cars.forEach(car => {
                    const carDiv = document.createElement('div');
                    carDiv.classList.add('car-item');
                    carDiv.innerHTML = `
                        <p><strong>Model:</strong> ${car.model}</p>
                        <p><strong>Price:</strong> $${car.price}</p>
                        <p><strong>Contact:</strong> ${car.contact_number}</p>
                        <img src="/static/uploads/${car.photo}" alt="Car Photo" class="car-photo">
                    `;
                    carsContainer.appendChild(carDiv);
                });
            } else {
                carsContainer.innerHTML = '<p>No cars added yet.</p>';
            }
        } else {
            alert('Failed to fetch cars. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching cars:', error);
    }
});
