document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/car-bookings');
        if (response.ok) {
            const data = await response.json();
            const carBookingsContainer = document.getElementById('carBookingsContainer');

            if (data.bookings.length > 0) {
                data.bookings.forEach(booking => {
                    const bookingDiv = document.createElement('div');
                    bookingDiv.classList.add('booking-item');
                    bookingDiv.innerHTML = `
                        <p><strong>Car Model:</strong> ${booking.car_model}</p>
                        <p><strong>Booking Date:</strong> ${booking.booking_date}</p>
                        <p><strong>Status:</strong> ${booking.status}</p>
                        <p><strong>Booked By:</strong> ${booking.booked_by}</p>
                        <p><strong>Contact:</strong> ${booking.booked_user_contact}</p>
                    `;
                    carBookingsContainer.appendChild(bookingDiv);
                });
            } else {
                carBookingsContainer.innerHTML = '<p>No bookings have been made on your cars yet.</p>';
            }
        } else {
            alert('Failed to fetch bookings. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching bookings:', error);
        alert('An error occurred while fetching bookings.');
    }
});
