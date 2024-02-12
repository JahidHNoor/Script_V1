const faucetWait = document.getElementById("manual_faucet-wait");
const timerFromModel = document.getElementById("timer-from-model");
const faucetTimer = document.getElementById("manual_faucet-timer");
const currentTime = document.getElementById("current-time");
const buttonText = document.getElementById("button-text");
const claimButton = document.getElementById("claim-button");
const claimButtonStyleChange = document.querySelector(".claim__button");


const timerValue = timerFromModel.textContent;
const timerM = Math.floor((timerValue / 60) % 60);
const timerS = Math.floor(timerValue % 60);
faucetTimer.innerHTML = timerM + " : " + timerS;

setInterval(() => {
  const faucetWaitUnix = Math.floor(faucetWait.textContent);

  const now = new Date().getTime();
  const curTime = Math.floor(now / 1000);
  currentTime.value = curTime;

  const diff = faucetWaitUnix - curTime;

  const m = Math.floor((faucetWaitUnix / 60 - curTime / 60) % 60);
  const s = Math.floor((faucetWaitUnix - curTime) % 60);

  if (diff > 0) {
    claimButton.disabled = true;
    // claimButton.disabled = false ;
    buttonText.innerHTML = m + " : " + s;
  } else if (diff == 0) {
    window.location.reload();
  } else {
    claimButton.disabled = false;
    claimButtonStyleChange.style.cursor = "pointer";
  }
}, 1000);

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}







// const roomNameInp = document.getElementById("room-id")
// const actionBtn = document.getElementById("actionBtn")
// roomNameInp.addEventListener('keyup', e => {
//     if (e.currentTarget.value == "") {
//         actionBtn.innerText = "Create New Room"
//     } else {
//         actionBtn.innerText = "Join"
//     }
// })   