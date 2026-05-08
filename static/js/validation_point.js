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

// Funngsi statistik
const button_set1 = document.getElementById("button_set1");
const button_set2 = document.getElementById("button_set2");
const button_set3 = document.getElementById("button_set3");
const button_all_set = document.getElementById("all");

const statistic_set1 = document.querySelectorAll(".stat_set1");
const statistic_set2 = document.querySelectorAll(".stat_set2");
const statistic_set3 = document.querySelectorAll(".stat_set3");
const statistic_all_set = document.querySelectorAll(".all_set");

// Fungsi untuk hide semua set
function hideAllSets() {
  [statistic_set1, statistic_set2, statistic_set3, statistic_all_set].forEach((set) => {
    set.forEach((el) => (el.style.display = "none"));
  });
}

// Tampilkan set_all tiap load
document.addEventListener("DOMContentLoaded", () => {
  hideAllSets();
  statistic_all_set.forEach((el) => (el.style.display = "block"));
});

// Event listener tombol
button_set1.addEventListener("click", () => {
  hideAllSets();
  statistic_set1.forEach((el) => (el.style.display = "block"));
  console.log("button 1 clicked");
});

button_set2.addEventListener("click", () => {
  hideAllSets();
  statistic_set2.forEach((el) => (el.style.display = "block"));
  console.log("button 2 clicked");
});

if (button_set3) {
  button_set3.addEventListener("click", () => {
    hideAllSets();
    statistic_set3.forEach((el) => (el.style.display = "block"));
    console.log("button 3 clicked");
  });
}

button_all_set.addEventListener("click", () => {
  hideAllSets();
  statistic_all_set.forEach((el) => (el.style.display = "block"));
  console.log("button all");
});
