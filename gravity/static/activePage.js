const navItem = document.querySelectorAll('a');
for (let i = 0; i < navItem.length; i++) {
    if (navItem[i].href === location.href) {
        navItem[i].classList.add('active');
    }
}