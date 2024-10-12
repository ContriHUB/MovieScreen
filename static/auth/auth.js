
(() => {
  const toast = document.querySelector(".message");
  setTimeout(() => {
    toast.style.display = "none";
  }, 4000);
})();
const toggle = document.querySelector('.pass-btn')
const input =toggle.parentElement.querySelector('input')
toggle.addEventListener(
  "click",
  (e) => {
    e.preventDefault();
    input.type === "password"
      ? (input.type = "text")
      : (input.type = "password");
    e.stopPropagation();
  },
  false
)