function load_css(fname) {
  $("<link/>", {
    rel: "stylesheet",
    type: "text/css",
    href: fname
  }).appendTo("head")
}

$(function() {
  $("#navibo").load("./src/html/footer.html", function() {load_css("./src/css/navibo.css")})
})
