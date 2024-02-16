document.addEventListener('DOMContentLoaded', function () {
  const foodBoxes = document.querySelectorAll('.food-box');
  const hoverWindow = document.getElementById('hoverWindow');
  const contentContainer = document.getElementById('contentContainer');
  const closeWindowBtn = document.getElementById('closeWindowBtn');

  foodBoxes.forEach(function (foodBox) {
    foodBox.addEventListener('click', function () {
	
	// Check if the clicked element is the heart button
	if (event.target.classList.contains('favorite-btn')) {
		return;
	}
	
      // Clear existing content
      contentContainer.innerHTML = '';

      // Break element
      const br = document.createElement('br');

      // Add ingredients text
      const ingredientsText = document.createElement('b');
      ingredientsText.innerHTML = "Ingredients";
      contentContainer.appendChild(ingredientsText);

      // Get the content associated with the clicked food box
      const ingredientList = foodBox.dataset.ingredientlist;

      try {
        // Try parsing the JSON
        ingredients = JSON.parse(ingredientList);

        // Add new content
        for (var i = 0; i < ingredients.length; i++) {
          const paragraph = document.createElement('p');
          paragraph.textContent = ingredients[i];
          contentContainer.appendChild(paragraph);
        }
      } catch (error) {
        // Handle parsing error
        console.error('Error parsing JSON:', error);
      }

      contentContainer.appendChild(br);

      // Add a button with link to recipe
      const recipeButton = document.createElement('button');
      const recipeURL = foodBox.dataset.recipeurl;
      try {
        // Try parsing the JSON
        recipe = JSON.parse(recipeURL);
        recipeButton.textContent = "View Recipe";
        recipeButton.onclick = function() {
          // window.location.href = recipe;
          window.open(recipe, "_blank")
        };
        contentContainer.appendChild(recipeButton);
      } catch (error) {
        // Handle parsing error
        console.error('Error parsing JSON:', error);
      }

      hoverWindow.style.display = 'block';
    });
  });

  closeWindowBtn.addEventListener('click', function () {
    hoverWindow.style.display = 'none';
  });
});
