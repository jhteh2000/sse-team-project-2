// Function to open modal
function openModal(action) {
    var modal = document.getElementById("createGroupModal");
    var modalTitle = document.getElementById("modalTitle");

    // Set modal title based on action
    if (action === 'create') {
        modalTitle.textContent = "Create Group";
    }
    // else {
    //     modalTitle.textContent = "Join Group";
    // }

    modal.style.display = "block";
}

// Function to close modal
function closeModal() {
    var modal = document.getElementById("createGroupModal");
    modal.style.display = "none";
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

// Function to handle accepting or declining an invitation
function handleInvitation(button, action) {
    // Get the table row
    var row = button.parentNode.parentNode;

    // Remove the row from the pending table
    row.parentNode.removeChild(row);
    
    // If the action is accept, move the row to the joined table
    if (action === 'accept') {
        var groupName = row.getElementsByTagName('td')[1].innerText;
        var description = row.getElementsByTagName('td')[2].querySelector('.view-description-btn').outerHTML;
        console.log(description);
        
        // Append the row to the "Joined Parties" table
        var joinedTable = document.getElementById("joined");
        var newRow = joinedTable.insertRow();
        newRow.innerHTML = '<td></td>' + // Auto-numbered column
                           '<td>' + groupName + '</td>' +
                           '<td>' + description + '</td>';
                           
        // Re-number the rows
        renumberRows(joinedTable);
        
        // Sort the table based on event date
        sortTableByDate(joinedTable);
    }
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

// Attach event listeners to the accept buttons
var acceptButtons = document.getElementsByClassName("accept-btn");
for (var i = 0; i < acceptButtons.length; i++) {
    acceptButtons[i].addEventListener("click", function() {
        handleInvitation(this, 'accept');
    });
}

// Attach event listeners to the decline buttons
var declineButtons = document.getElementsByClassName("decline-btn");
for (var i = 0; i < declineButtons.length; i++) {
    declineButtons[i].addEventListener("click", function() {
        handleInvitation(this, 'decline');
    });
}
