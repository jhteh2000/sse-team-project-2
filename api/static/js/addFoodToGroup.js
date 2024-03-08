function addToGroup(){

    const userEmail = document.getElementById('userProfileContainer').getAttribute('data-user-email');
    var dishUri = event.target.closest('.food-box').getAttribute('data-uri');
    
    var foodData = {
        userEmail : userEmail,
        dishUri : JSON.parse(dishUri)
    };

    var jsonData = JSON.stringify(foodData);

    console.log('JSON data sent:', jsonData);

    // 'http://127.0.0.1:3000' // change to this url when testing locally
    fetch('http://127.0.0.1:3000/add-food-to-groups', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: jsonData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        alert(data['message']);
        closeModal();
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
