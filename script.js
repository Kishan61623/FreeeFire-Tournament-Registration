document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registrationForm');
    const successMessage = document.getElementById('successMessage');
    const squadNumberSpan = document.getElementById('squadNumber');

    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const squadName = document.getElementById('squadName').value;
        const mobileNumber = document.getElementById('mobileNumber').value;

        // Generate a unique Squad No
        const squadNo = generateSquadNumber();

        const registrationData = {
            name,
            squadName,
            mobileNumber,
            squadNo,
            timestamp: new Date().toISOString()
        };

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registrationData)
            });

            const result = await response.json();

            if (response.ok) {
                squadNumberSpan.textContent = result.squadNo;
                registrationForm.reset();
                registrationForm.classList.add('hidden');
                successMessage.classList.remove('hidden');
                console.log('Registration successful:', result);
            } else {
                alert(result.message || 'Registration failed. Please try again.');
                console.error('Registration failed:', result);
            }
        } catch (error) {
            console.error('Network error or server issue:', error);
            alert('An error occurred during registration. Please try again later.');
        }
    });

    function generateSquadNumber() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < 6; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result;
    }
});