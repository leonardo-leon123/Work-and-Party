const slidePage = document.querySelector(".slidepage");
const firstNextBtn = document.querySelector(".nextBtn");
// const prevBtnSec = document.querySelector(".prev-1");
// const nextBtnSec = document.querySelector(".next-1");
const prevBtnThrid = document.querySelector(".prev-2");
const nextBtnThrid = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");

let max = 4;
let current = 1;

firstNextBtn.addEventListener("click", function()
{
    slidePage.style.marginLeft = "-25%";
    bullet[current - 1].classList.add("active")
    progressText[current - 1].classList.add("active")
    progressCheck[current - 1].classList.add("active")
    current +=1;
});


// nextBtnSec.addEventListener("click", function()
// {
//     slidePage.style.marginLeft = "-50%";
//     bullet[current - 1].classList.add("active")
//     progressText[current - 1].classList.add("active")
//     progressCheck[current - 1].classList.add("active")
//     current +=1;
// });

// prevBtnSec.addEventListener("click", function()
// {
//     slidePage.style.marginLeft = "0%";
//     bullet[current - 2].classList.remove("active")
//     progressText[current - 2].classList.remove("active")
//     progressCheck[current - 2].classList.remove("active")
//     current -=1;
// });


nextBtnThrid.addEventListener("click", function()
{
    slidePage.style.marginLeft = "-50%";
    bullet[current - 1].classList.add("active")
    progressText[current - 1].classList.add("active")
    progressCheck[current - 1].classList.add("active")
    current +=1;
});
prevBtnThrid.addEventListener("click", function()
{
    slidePage.style.marginLeft = "0%";
    bullet[current - 2].classList.remove("active")
    progressText[current - 2].classList.remove("active")
    progressCheck[current - 2].classList.remove("active")
    current -=1;
});


prevBtnFourth.addEventListener("click", function()
{
    slidePage.style.marginLeft = "-25%";
    bullet[current - 2].classList.remove("active")
    progressText[current - 2].classList.remove("active")
    progressCheck[current - 2].classList.remove("active")
    current -=1;
});





// Drop down from w3 --- Get all elements with class="closebtn"
var close = document.getElementsByClassName("closebtn");
var i;

// Loop through all close buttons
for (i = 0; i < close.length; i++) {
  // When someone clicks on a close button
  close[i].onclick = function(){

    // Get the parent of <span class="closebtn"> (<div class="alert">)
    var div = this.parentElement;

    // Set the opacity of div to 0 (transparent)
    div.style.opacity = "0";

    // Hide the div after 600ms (the same amount of milliseconds it takes to fade out)
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect); 