// Function to open modal
function openModal(action) {
    var modal = document.getElementById("createGroupModal");
    var modalTitle = document.getElementById("modalTitle");

    // Set modal title based on action
    if (action === 'create') {
        modalTitle.textContent = "Create Group";
    }
    // } else {
    //     modalTitle.textContent = "Join Group";
    // }

    modal.style.display = "block";
}

// Function to close modal
function closeModal() {
    var modal = document.getElementById("createGroupModal");
    modal.style.display = "none";
}

// Placeholder function for logout
function logout() {
    alert("Logout functionality will be implemented here.");
    // Add logout functionality here
}