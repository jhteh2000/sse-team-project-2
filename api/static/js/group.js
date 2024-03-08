function openModal(action) {
    var modal = document.getElementById("createGroupModal");
    var modalTitle = document.getElementById("modalTitle");

    // Set modal title based on action
    if (action === 'create') {
        modalTitle.textContent = "Create Group";
    }

    // Clear previous form input values
    document.getElementById("createGroupForm").reset();

    modal.style.display = "block";
}

// Function to close modal
function closeModal() {
    var modal = document.getElementById("createGroupModal");
    modal.style.display = "none";
}

// Function to handle form submission
function submitGroup() {
    var groupName = document.getElementById("groupName").value;
    var groupDetail = document.getElementById("groupDetail").value;

    // Retrieve the value of userEmail from the hidden input
    var userEmail = document.getElementById('userEmail').value;
    // Split the groupMembers string by ';' to create an array of emails
    var groupMembers = document.getElementById("groupMembers").value.split(';').map(function(email) {
        return email.trim(); // Trim whitespace from each email
    });

    // Prepend the userEmail to the groupMembers array
    var memberList = [userEmail].concat(groupMembers);

    console.log(memberList);


    var groupData = {
        groupName: groupName,
        groupDetail: groupDetail,
        groupMembers: memberList
    };

    var jsonData = JSON.stringify(groupData);

    console.log('JSON data sent:', jsonData);

    // 'http://127.0.0.1:3000' // change to this url when testing locally
    fetch('http://127.0.0.1:3000/create-group', {
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
        closeModal(); 
        window.location.reload(); 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function openDescriptionModal(action, index) {
    console.log("openDescriptionModal called with action:", action, "and index:", index);

    var descriptionModal = document.getElementById("groupDescriptionModal");
    var descriptionContent = document.getElementById("groupDescription");

    // Set modal content based on action
    if (action === 'openDescription') {
        //var n = parseInt(index);
        var description = index.description;
        console.log("Description:", description);
        descriptionContent.textContent = description;
    }

    // Display the modal
    descriptionModal.style.display = "block";
}

function closeDescriptionModal() {
    var descriptionModal = document.getElementById("groupDescriptionModal");
    descriptionModal.style.display = "none";
}

// Placeholder function for logout
function logout() {
    alert("Logout functionality will be implemented here.");
    // Add logout functionality here
}

// Function to retrieve the event date based on the group name
function getEventDate(groupName) {
    // Placeholder implementation, you should replace this with actual date retrieval logic
    return "01/01/2025"; // Placeholder date
}

// Function to renumber rows in the table
function renumberRows(table) {
    var rows = table.getElementsByTagName('tr');
    for (var i = 1; i < rows.length; i++) {
        rows[i].getElementsByTagName('td')[0].innerText = i;
    }
}

// Function to sort the table by event date
function sortTableByDate(table) {
    var rows = Array.prototype.slice.call(table.rows, 1); // Exclude header row
    rows.sort(function(a, b) {
        var date1 = new Date(a.cells[2].innerText);
        var date2 = new Date(b.cells[2].innerText);
        return date1 - date2;
    });
    rows.forEach(function(row) {
        table.appendChild(row);
    });
}

function handleInvitationResponse(groupId, userEmail, action) {
    // Determine the correct URL based on the action
    // 'http://127.0.0.1:3000' // change to this url when testing locally
    var url = action === 'accept' 
        ? 'http://127.0.0.1:3000/accept-group' 
        : 'http://127.0.0.1:3000/decline-group';
        console.log(url);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ group_id: groupId, email: userEmail }),
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

// Attach event listeners to the accept buttons
var acceptButtons = document.getElementsByClassName("accept-btn");
for (var i = 0; i < acceptButtons.length; i++) {
    acceptButtons[i].addEventListener("click", function() {
        var groupId = this.getAttribute('data-group-id');
        var userEmail = this.getAttribute('data-user-email');
        handleInvitationResponse(groupId, userEmail, 'accept');
    });
}

// Attach event listeners to the decline buttons
var declineButtons = document.getElementsByClassName("decline-btn");
for (var i = 0; i < declineButtons.length; i++) {
    declineButtons[i].addEventListener("click", function() {
        var groupId = this.getAttribute('data-group-id');
        var userEmail = this.getAttribute('data-user-email');
        handleInvitationResponse(groupId, userEmail, 'decline');
    });
}

function handleRemoveGroupResponse(groupId, userEmail) {
    console.log(groupId);
    console.log(userEmail);
    
    // 'http://127.0.0.1:3000' // change to this url when testing locally
    var url = 'http://127.0.0.1:3000/remove-group';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ group_id: groupId, email: userEmail }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(`response:`, data);
        // Reload the page to reflect changes
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach event listeners to the remove-group buttons
var removeGroupButtons = document.getElementsByClassName("remove-group-btn");
for (var i = 0; i < removeGroupButtons.length; i++) {
    removeGroupButtons[i].addEventListener("click", function() {
        var groupId = this.getAttribute('data-group-id');
        var userEmail = this.getAttribute('data-user-email');
        handleRemoveGroupResponse(groupId, userEmail);
    });
}
