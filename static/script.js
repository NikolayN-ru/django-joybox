let btn = document.querySelector(".mobileMenu");
let menu = document.querySelector(".mobileMenuItems");
mobileMenu = document.querySelector(".mobileMenu");
btn.onclick = () => {
  menu.classList.toggle("mobileMenuItemsShow");
  mobileMenu.classList.toggle("mobileMenuActive");
};
