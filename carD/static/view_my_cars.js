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
                        <div class="car-actions">
                            <button onclick="deleteCar(${car.id})">Delete Car</button>
                            <button onclick="editCar(${car.id})">Edit Car</button>
                        </div>
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
        alert('An error occurred while fetching your cars.');
    }
});

async function deleteCar(carId) {
    if (confirm('Are you sure you want to delete this car?')) {
        try {
            const response = await fetch(`/api/delete-car/${carId}`, {
                method: 'DELETE'
            });
            const responseData = await response.json();
            if (response.ok) {
                console.log(responseData);
                alert('Car deleted successfully!');
                setTimeout(() => {
                    location.reload();
                }, 1800);
            } else {
                console.log(responseData); 
                alert('Failed to delete car. Please try again.');
            }
        } catch (error) {
            console.error('Error deleting car:', error);
            alert('An error occurred while deleting the car.');
        }
    }
}

async function editCar(carId) {
    try {
        const response = await fetch(`/api/get-car/${carId}`);
        if (response.ok) {
            const car = await response.json();
            console.log('Car details fetched for editing:', car);
        } else {
            alert('Failed to fetch car details. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching car details:', error);
        alert('An error occurred while fetching car details.');
    }
}
