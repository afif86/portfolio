document.querySelectorAll(".burger, .overlay").forEach((element) => {
  element.addEventListener("click", () => {
    document.querySelector(".burger").classList.toggle("clicked");
    document.querySelector(".overlay").classList.toggle("show");
    document.querySelector("nav").classList.toggle("show");
    document.querySelector("body").classList.toggle("overflow");
  });
});
