document.addEventListener('DOMContentLoaded', async () => {
    await fetchAndDisplayCars(); // Fetch all cars initially
});

async function fetchAndDisplayCars(query = '') {
    try {
        // Fetch the available cars from the server
        const response = await fetch(`/api/available-cars${query ? `?query=${encodeURIComponent(query)}` : ''}`);
        
        if (response.ok) {
            const data = await response.json();
            const carsContainer = document.getElementById('carsContainer');

            // Clear previous results
            carsContainer.innerHTML = '';

            // Check if there are any available cars
            if (data.cars.length > 0) {
                data.cars.forEach(car => {
                    // Create a card for each car
                    const carDiv = document.createElement('div');
                    carDiv.classList.add('car-item');
                    carDiv.innerHTML = `
                        <img src="/static/uploads/${car.photo}" alt="Car Photo" class="car-photo">
                        <p><strong>Model:</strong> ${car.model}</p>
                        <p><strong>Price:</strong> $${car.price}</p>
                        <p><strong>Contact:</strong> ${car.contact_number}</p>
                        <div class="car-actions">
                            <button onclick="bookCar(${car.id})">Book Car</button>
                        </div>
                    `;
                    carsContainer.appendChild(carDiv);
                });
            } else {
                carsContainer.innerHTML = '<p>No cars available for booking.</p>';
            }
        } else {
            alert('Failed to fetch available cars. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching available cars:', error);
        alert('An error occurred while fetching available cars.');
    }
}

async function searchCars() {
    const query = document.getElementById('searchQuery').value.trim();
    if (!query) {
        alert('Please enter a search term');
        return;
    }
    await fetchAndDisplayCars(query);
}

// Function to book a car
async function bookCar(carId) {
    try {
        const response = await fetch(`/api/book-car/${carId}`, {
            method: 'POST'
        });
        if (response.ok) {
            alert('Car booked successfully!');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            alert('Failed to book car. Please try again.');
        }
    } catch (error) {
        console.error('Error booking car:', error);
        alert('An error occurred while booking the car.');
    }
}
