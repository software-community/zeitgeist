var login_but = false;

$(".arrow").click(function () {
  $('.stage-front-wrap').css('transform','translateY(0) translateX(0)')
  $(".but-cont").css("opacity", "0");
});

$(".but").click(function () {
  if (login_but==false){
    login_but=true;
    $('.login-but').css("display","block")
    setTimeout(function(){
      $('.login-but').css("opacity","1")
    },30)
    setTimeout(function(){
      $('.login-but').css("opacity","0")
    },3500)
    setTimeout(function(){
      $('.login-but').css("display","none")
      login_but=false
    },3900)
  }
  $(".stage-front-wrap").css("transition", "transform 0.1s ease-in-out");
  $(".stage-front-wrap").css("transform", "translateX("+(25).toString()+'px)');
  setTimeout(function(){
    $(".stage-front-wrap").css("transform", "translateX("+(-25).toString()+'px)');
  },100)
  setTimeout(function(){
    $(".stage-front-wrap").css("transform", "translateX("+(25).toString()+'px)');
  },200)
  setTimeout(function(){
    $(".stage-front-wrap").css("transform", "translateX("+(-25).toString()+'px)');
  },300)
  setTimeout(function(){
    $(".stage-front-wrap").css("transform", "translateX("+(0).toString()+'px)');
  },400)
});
