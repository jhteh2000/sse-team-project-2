document.addEventListener('DOMContentLoaded', function() {
    const userGreeting = document.getElementById('user-greeting');
    const loginButton = document.getElementById('login');
    const registerButton = document.getElementById('register');
    const logoutButton = document.getElementById('logout');

    // Check if the user is logged in
    const isLoggedIn = localStorage.getItem('userLoggedIn') === 'true';

    // Display user's first name if logged in
    if (isLoggedIn) {
        const firstName = localStorage.getItem('userFirstName');
        userGreeting.textContent = `Hello, ${firstName}!`;
    }

    // Toggle visibility of login, register, and logout buttons
    loginButton.style.display = isLoggedIn ? 'none' : 'inline-block';
    registerButton.style.display = isLoggedIn ? 'none' : 'inline-block';
    logoutButton.style.display = isLoggedIn ? 'inline-block' : 'none';

    // Logout functionality
    logoutButton.addEventListener('click', function() {
        // Clear user-related data on logout
        localStorage.removeItem('userLoggedIn');
        localStorage.removeItem('userFirstName');

        // Redirect to the login page
        window.location.href = 'login.html';
    });
});
