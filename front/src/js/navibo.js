function _add_random(name) {
  return name + "?v=" + Math.random()
}

function load_css(fname) {
  $("<link/>", {
    rel: "stylesheet",
    type: "text/css",
    href: _add_random(fname)
  }).appendTo("head")
}

function load_data(url) {
  $.ajax({url: url, method: 'POST'})
    .then(function(data) {
      console.log(data)
    })
}

function load_binds() {
  $(".navibo-ontoggle").on("click", function() {
    $(".navibo-toggle").toggle()
  })
}

$(function() {
  const cID = $("#navibo").data("id")
  const jsondaata = load_data("http://localhost:5000/navibo/" + cID)
  $("#navibo").load(
    _add_random("./src/html/footer.html"),
    function() {
      load_css(_add_random("./src/css/navibo.css"))
      load_binds()
    })
})
