// Inisialiasi Form submit
const pointForm = document.getElementById("pointForm");

pointForm.addEventListener("submit", function (e) {
  // Inisialisasi serve_type dan point
  const serveChecked = document.querySelector("input[name='serve_type']:checked");
  const pointChecked = document.querySelector("input[name='point']:checked");

  // Jika salah satunya belum dipilih, hentikan submit
  if (!serveChecked || !pointChecked) {
    e.preventDefault(); // hentikan form submit
    Swal.fire({
      icon: "error",
      text: "Pick winner point and serve type",
      confirmButtonText: "Ok",
      background: "#151c27",
      color: "#ffffff",
      confirmButtonColor: "#00ff08",
    });
    return;
  }
});

function confirm_cancel() {
  Swal.fire({
    background: "#151c27",
    text: "Cancel point terakhir?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Ya",
    cancelButtonText: "Tidak",
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById("cancelForm").submit();
    }
  });
}
