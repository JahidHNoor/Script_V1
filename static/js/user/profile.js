const currentTime = document.getElementById("current-time");
const progressPercentModel = document.getElementById("progress_percent");
const progressPercent = progressPercentModel.textContent;



let progressBar = document.querySelector(".circular-progress");
let valueContainer = document.querySelector(".value-container");

let progressValue = -1;
let progressEndValue = progressPercent;
let speed = 30;

let progress = setInterval(() => {
  progressValue++;
  valueContainer.textContent = `${progressValue}%`;
  progressBar.style.background = `conic-gradient(
      #4d5bf9 ${progressValue * 3.6}deg,
      #aec7fa ${progressValue * 3.6}deg
  )`;


  if (progressValue == progressEndValue) {
    clearInterval(progress);
  } 
}, speed);

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

setInterval(() => {

  const now = new Date().getTime();
  const curTime = Math.floor(now / 1000);
  currentTime.value = curTime;


}, 1000);