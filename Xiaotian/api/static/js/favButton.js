document.addEventListener('DOMContentLoaded', function () {
  const favoriteButtons = document.querySelectorAll('.favorite-btn');

  favoriteButtons.forEach((button) => {
    button.addEventListener('click', function () {
      // Toggle the "active" class to change the color
      button.classList.toggle('active');
    });
  });
});

