$('.arrow').click(function(){
  $('.stage-front-wrap').css('transform','translateY(0) translateX(0)')
  $('.but-cont').css('opacity','0')
})

$('.but1').click(function(){
  $('.stage-front-wrap').css('transform','translateY(100vh)')
  setTimeout(function(){
  $('.but1-cont').css('opacity','1')
  },400);
})

$('.but2').click(function(){
  $('.stage-front-wrap').css('transform','translateY(-100vh)')
  setTimeout(function(){
  $('.but2-cont').css('opacity','1')
  },400);
})

$('.but3').click(function(){
  $('.stage-front-wrap').css('transform','translateX(100vw)')
  setTimeout(function(){
  $('.but3-cont').css('opacity','1')
  },400);
})

$('.but4').click(function(){
  $('.stage-front-wrap').css('transform','translateX(-100vw)')
  setTimeout(function(){
  $('.but4-cont').css('opacity','1')
  },400);
})