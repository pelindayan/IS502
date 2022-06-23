$(() => {
  $('a[href*="#"]:not([href="#"])').click(e => {
    const target = $(e.target.hash);

    if (target.length) {
      $('html, body').animate({
        scrollTop: target.offset().top },
      1000);

      return false;
    }
  });
});

function checkCookie(){
  let x = document.cookie;
  if (x == '') {
    window.location.replace("http://metuchatbot.com/login/?#");
  }else{
    window.location.replace("http://metuchatbot.com/chatbot");
  }
}