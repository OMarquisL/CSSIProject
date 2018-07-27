
function hide(someId) {
  var x = document.getElementById(someId);
  if (x) {
    x.style.display = "none";
  } else {
    console.log("Nothing found for " + someId);
  }
}

function show(someId) {
  var x = document.getElementById(someId);
  if (x) {
    x.style.display = "block";
  } else {
    console.log("Nothing found for " + someId);
  }
}

function toggle(someId) {
  var x = document.getElementById(someId);
  if (x) {
    if (x.style.display == 'block') {
      x.style.display = "none";
    } else {
      x.style.display = 'block';
    }
  } else {
    console.log("Nothing found for " + someId);
  }
}
