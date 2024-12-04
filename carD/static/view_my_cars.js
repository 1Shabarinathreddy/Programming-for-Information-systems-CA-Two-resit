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
            const editFormHtml = `
                <div class="edit-car-form">
                    <h3>Edit Car</h3>
                    <form id="editCarForm">
                        <input type="text" id="editModel" value="${car.model}" required>
                        <input type="text" id="editPrice" value="${car.price}" required>
                        <input type="tel" id="editContact" value="${car.contact_number}" required>
                        <button type="submit">Save Changes</button>
                    </form>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', editFormHtml);

            document.getElementById('editCarForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const updatedCar = {
                    model: document.getElementById('editModel').value,
                    price: document.getElementById('editPrice').value,
                    contact_number: document.getElementById('editContact').value
                };
                try {
                    const updateResponse = await fetch(`/api/update-car/${carId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(updatedCar)
                    });
                    if (updateResponse.ok) {
                        alert('Car updated successfully!');
                        location.reload();
                    } else {
                        alert('Failed to update car. Please try again.');
                    }
                } catch (error) {
                    console.error('Error updating car:', error);
                    alert('An error occurred while updating the car.');
                }
            });
        } else {
            alert('Failed to fetch car details. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching car details:', error);
        alert('An error occurred while fetching car details.');
    }
}
