function resetForm() {
  window.location.href = "/?reset=1";
}
function validateAndShowPopup() {
  let p1 = document.getElementById("p1").value;
  let p2 = document.getElementById("p2").value;
  let finalSet = document.getElementById("final_set_scoring").value;

  if (!p1 || !p2 || p1 === p2 || !finalSet) {
    alert("⚠️ Pick 2 different players and method last set!!");
    return;
  }

  showPopup(); 
  
function showPopup() {
  let p1 = document.getElementById("p1").value;
  let p2 = document.getElementById("p2").value;
  let finalSet = document.getElementById("final_set_scoring").value;

  let finalSetText = {
    normal: "Normal Set",
    super_tiebreak: "Super Tiebreak (6–6)",
    super_tiebreak_only: "Super Tiebreak Only",
  };

  document.getElementById("popup_p1").innerText = p1;
  document.getElementById("popup_p2").innerText = p2;
  document.getElementById("popup_final").innerText = "Final Set: " + finalSetText[finalSet];

  document.getElementById("overlay").style.display = "block";
  let popup = document.getElementById("popup");
  popup.style.display = "block";

  // animasi masuk
  setTimeout(() => {
    popup.classList.add("show");
  }, 10);
}

function closePopup() {
  let popup = document.getElementById("popup");

  popup.classList.remove("show");

  setTimeout(() => {
    popup.style.display = "none";
    document.getElementById("overlay").style.display = "none";
  }, 200);
}

function confirmMatch() {
  closePopup(); // tutup popup pertama
  showServerPopup(); // buka popup kedua
}

function showServerPopup() {
  document.getElementById("overlay").style.display = "block";

  let popup = document.getElementById("popup-server");
  popup.style.display = "block";

  setTimeout(() => {
    popup.classList.add("show");
  }, 10);
}

function closeServerPopup() {
  let popup = document.getElementById("popup-server");

  popup.classList.remove("show");

  setTimeout(() => {
    popup.style.display = "none";
    document.getElementById("overlay").style.display = "none";
  }, 200);
}

function setFirstServer(player) {
  document.getElementById("first_server").value = player;

  let form = document.getElementById("playerForm");
  let formData = new FormData(form);

  console.log("FORM DATA:");
  for (let [key, value] of formData.entries()) {
    console.log(key, ":", value);
  }

  form.requestSubmit();
}
