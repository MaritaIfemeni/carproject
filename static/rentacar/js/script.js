//For the to "TOP" button
var mybutton = document.getElementById("myBtn");
// When scrolled down 20px from top, shows the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
    } else {
    mybutton.sdisplay = "none";
    }
}
// Onclick, scrolls top
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}