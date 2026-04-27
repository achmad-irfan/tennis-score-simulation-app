const matchType = document.querySelectorAll("input[name='match']");
const single = document.querySelector(".single-player");
const double = document.querySelector(".double-player");

function toggleMatchType() {
  const selected = document.querySelector('input[name="match"]:checked').value;

  if (selected === "single") {
    single.style.display = "block";
    double.style.display = "none";
  } else {
    single.style.display = "none";
    double.style.display = "flex";
  }
}

// initial state
toggleMatchType();

// event listener
matchType.forEach((radio) => {
  radio.addEventListener("change", toggleMatchType);
});
