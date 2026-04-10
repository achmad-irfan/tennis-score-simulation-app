function showError(message) {
  if (!message) return;
  Swal.fire({
    icon: "error",
    text: message,
    confirmButtonText: "Ok",
    background: "#151c27",
    color: "#ffffff",
    iconColor: "#ffffff",
    confirmButtonColor: "#00ff08",
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const errorElem = document.getElementById("error-msg");
  if (errorElem) {
    showError(errorElem.dataset.message);
  }
});
