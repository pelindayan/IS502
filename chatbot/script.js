var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}
function checkCookie(){
  let x = document.cookie;
  if (x == '') {
    window.location.replace("http://metuchatbot.com/login/?#");
  }
}
function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
    // fakeMessage();
    getAnswerFromChatBot(msg);
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var Fake = [
  'Hi I am your METU Assistant, at your service'
]

function fakeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../assets/odtulogo.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="../assets/odtulogo.png" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
  }, 1000 + (Math.random() * 20) * 100);

}

function getAnswerFromChatBot(msg) {
  var greetings = ['hi','hello','hey', 'how are you', 'hi there'];
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../assets/odtulogo.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
  if (greetings.includes(msg.toLowerCase())) {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="../assets/odtulogo.png" /></figure>How can i help you today?</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
  } else {
    user = document.cookie;
    text = msg.concat("$", user);
    var params = { "text" : msg,
                   "user" : document.cookie
    };
    fetch("http://metuchatbot.com:8000/predict", { 
      method: "POST",
      headers: {
        Accept: "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(params)
      }).then((Response) => {
          return Response.json()
      }).then((data) => {
      $('.message.loading').remove();
      if (data.response.includes("Link: ")) {
        var link = data.response.substring(data.response.indexOf('Link: ') + 6);
        var text = data.response.substring(0, data.response.indexOf('Link: ') + 6);
      }else{
        var link = "";
        var text = data.response;
      }
      $('<div class="message new"><figure class="avatar"><img src="../assets/odtulogo.png" /></figure>'+text+'<a href="'+link+'" target="_blank" style="color:white">' + link + '</a></div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
        })
  }
}