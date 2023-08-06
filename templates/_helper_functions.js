
// Auto removes alert messages after 5 seconds
setTimeout(function () {
    document.querySelector(".alert").remove();
}, 5000);

// Enables flashing a login error message from any route via JS
function showLoginError() {
    window.location.href = "/login-error";
}

// Accepts a drinkId and and adds it to the collectionsModal.data attribute
function setDrinkId(drinkId) {
    $("#collectionsModal").data("drinkId", drinkId);
}