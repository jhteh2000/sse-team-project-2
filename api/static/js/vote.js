function handleVoteResponse(groupId, userEmail, dishUri, action) {
    // Determine the correct URL based on the action
    var url = action === 'vote' 
        ? 'http://127.0.0.1:3000/click-vote-dish' 
        : 'http://127.0.0.1:3000/cancel-vote-dish';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ groupId: groupId, userEmail: userEmail, dishUri: dishUri }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(`${action} response:`, data);
        // Reload the page to reflect changes
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach event listeners to the vote buttons
var voteButtons = document.getElementsByClassName("vote-btn");
for (var i = 0; i < voteButtons.length; i++) {
    voteButtons[i].addEventListener("click", function() {
        var groupId = this.getAttribute('data-group-id');
        var userEmail = this.getAttribute('data-user-email');
        var dishUri = this.getAttribute('data-dish-uri');
        handleVoteResponse(groupId, userEmail, dishUri, 'vote');
    });
}

// Attach event listeners to the cancel vote buttons
var cancelButtons = document.getElementsByClassName("cancel-btn");
for (var i = 0; i < cancelButtons.length; i++) {
    cancelButtons[i].addEventListener("click", function() {
        var groupId = this.getAttribute('data-group-id');
        var userEmail = this.getAttribute('data-user-email');
        var dishUri = this.getAttribute('data-dish-uri');
        handleVoteResponse(groupId, userEmail, dishUri, 'cancel-vote');
    });
}
