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

function init_navibo() {
  $(".navibo-ontoggle").on("click", function() {
    const duration = 100
    if ($(".navibo-open").is(":visible")) {
      $(".navibo-open").toggle(duration, function() {
        $(".navibo-balloon").toggle(duration)
      })
    } else {
      $(".navibo-balloon").toggle(duration, function() {
        $(".navibo-open").toggle(duration)
      })
    }
  })
}

function navibo_choice(question_id, answer_id) {
  const new_records = JSON.parse(sessionStorage.getItem("navibo-records"))
  new_records.push([question_id, answer_id])
  set_navibo(new_records)
}

function _set_question(question) {
  $("<p>", {
    text: question.question
  }).appendTo(".navibo-contents")
}

function _set_answers(question) {
  if(question.answer_type == "choice") {
    question.answers.map(function(answer) {
      $("<label>", {
        text: answer.answer_text,
        class: "navibo-button",
        onClick: "navibo_choice(" + question.question_id + ", " + answer.answer_id + ")"
      }).appendTo(".navibo-contents")
    })
  }
}

function _set_item(item) {
  $("<p>", {
    text: item.item_name
  }).appendTo(".navibo-contents")
  $("<p>", {
    class: "navibo-description",
    text: item.item_description
  }).appendTo(".navibo-contents")
}

function set_content(content, is_question) {
  if(is_question) {
    _set_question(content.question)
    _set_answers(content.question)
  } else {
    _set_item(content.item)
  }
}

function set_navibo(records) {
  const cID = $("#navibo").data("id")
  const url = "http://localhost:5000/navibo/" + cID
  const records_json = JSON.stringify(records)
  $(".navibo-contents").html("")
  $.ajax({
    url: url, method: 'POST', data: records_json, contentType: 'application/json'
  }).then(function(data) {
    const jsondata = JSON.parse(data)
    console.log(jsondata)
    set_content(jsondata.content, jsondata.is_question)
  })
  sessionStorage.setItem("navibo-records", records_json)
}

$(function() {
  $("#navibo").load(
    _add_random("./src/html/footer.html"),
    function() {
      load_css(_add_random("./src/css/navibo.css"))
      init_navibo()
      set_navibo([])
    })
})
