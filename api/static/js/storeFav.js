document.addEventListener("DOMContentLoaded", function () {
  // Get all favorite buttons
  var favoriteButtons = document.querySelectorAll(".favorite-btn");

  // Add click event listener to each favorite button
  favoriteButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      // Toggle the 'active' class to change the color
      button.classList.toggle("active");

      // Get the parent food box
      var foodBox = button.closest(".food-box");

      // Retrieve data attributes from the food box
      var recipeuri = foodBox.getAttribute("data-uri");

      // Create an object with the retrieved data
      var foodData = {
        uri: JSON.parse(recipeuri)
      };

      // Log the data or send it to the backend
      console.log(foodData);

      // Send the data to the backend using an AJAX request
      if (button.classList.contains("active")) {
        fetch('/add_selected_food', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(foodData),
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          // Optionally update the UI or perform additional actions
        })
        .catch((error) => {
          console.error('Error:', error);
          // Handle errors or display an error message
        });
      } else {
        fetch('/remove_selected_food', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(foodData),
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success (Remove):', data);
          // Optionally update the UI or perform additional actions
        })
        .catch((error) => {
          console.error('Error (Remove):', error);
          // Handle errors or display an error message
        });
      } 
    });
  });
});

