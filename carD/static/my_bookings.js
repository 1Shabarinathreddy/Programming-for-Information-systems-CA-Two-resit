document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/my-bookings');
        if (response.ok) {
            const data = await response.json();
            const myBookingsContainer = document.getElementById('myBookingsContainer');

            if (data.bookings.length > 0) {
                data.bookings.forEach(booking => {
                    const bookingDiv = document.createElement('div');
                    bookingDiv.classList.add('booking-item');
                    bookingDiv.innerHTML = `
                        <p><strong>Car Model:</strong> ${booking.car_model}</p>
                        <p><strong>Booking Date:</strong> ${booking.booking_date}</p>
                        <p><strong>Status:</strong> ${booking.status}</p>
                        <p><strong>Car Owner:</strong> ${booking.owner_name}</p>
                        <p><strong>Contact:</strong> ${booking.owner_contact}</p>
                    `;
                    myBookingsContainer.appendChild(bookingDiv);
                });
            } else {
                myBookingsContainer.innerHTML = '<p>You have not made any bookings yet.</p>';
            }
        } else {
            alert('Failed to fetch bookings. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching bookings:', error);
        alert('An error occurred while fetching your bookings.');
    }
});
