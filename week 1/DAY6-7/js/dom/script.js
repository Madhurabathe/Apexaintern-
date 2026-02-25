let button = document.getElementById("colorBtn");

button.onclick = function() {
    let colors = ["red", "blue", "green","black","yellow","pink","purple","orange","cyan","magenta"];

    document.body.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
};