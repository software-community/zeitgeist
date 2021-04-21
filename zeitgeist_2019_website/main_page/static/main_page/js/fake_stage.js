var login_but = false;

$(".arrow").click(function () {
  $(".stage-front").css("margin-top", "-5%");
  $(".stage-front").css("margin-left", "-10%");
  $(".but-cont").css("opacity", "0");
});

$(".but").click(function () {
  $(".stage-front").css("transition", "margin 0.2s ease-in-out");
  $(".stage-front").css("margin-left", (-0.1*screen.width+25).toString()+'px');
  setTimeout(function(){
    $(".stage-front").css("margin-left", (-0.1*screen.width-25).toString()+'px');
  },200)
  setTimeout(function(){
    $(".stage-front").css("margin-left", (-0.1*screen.width+25).toString()+'px');
  },400)
  setTimeout(function(){
    $(".stage-front").css("margin-left", (-0.1*screen.width-25).toString()+'px');
  },600)
  setTimeout(function(){
    $(".stage-front").css("margin-left", (-0.1*screen.width).toString()+'px');
  },800)
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
});
