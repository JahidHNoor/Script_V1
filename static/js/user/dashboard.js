// Copy Referral Link
let referralBox = document.getElementById("referral-link");
let referralButton = document.getElementById("referral-btn");
let changeCopyText = document.getElementById("copy-referral");

referralButton.onclick = function () {
  referralBox.select();
  document.execCommand("copy");
  changeCopyText.innerText = "Codes Copied";
};

// Hide and Show Referral Rewards Claim Button
const claimButton = document.getElementById("claim-button");
const claimButtonDiv = document.getElementById("claim-button-div");
const referralRewardsAmount = document.getElementById("referral-rewards-amount");

const referralRewards = referralRewardsAmount.textContent;

if (referralRewards == 0) {
  claimButton.disabled = true;
  claimButtonDiv.style.display = "none";
} else {
  claimButton.disabled = false;
  claimButtonDiv.style.cursor = "pointer";
  claimButtonDiv.style.display = "flex";
}
