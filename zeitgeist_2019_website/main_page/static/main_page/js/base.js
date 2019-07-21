$(document).ready(function(){
    $(".buttona a").click(function(){
        $(".overlay").fadeToggle(200);
       $(this).toggleClass('btn-opena').toggleClass('btn-closea');
    });
});
$('.overlay').on('click', function(){
    $(".overlay").fadeToggle(200);
    $(".buttona a").toggleClass('btn-opena').toggleClass('btn-closea');
    open = false;
});
