$(".page1 .card-wrap").click(function() {
  var id = this.id;
  alert(id);
  $(".page1").css("display", "none");
  $("." + id).css("display", "block");
});

$(".eachdept").click(function() {
  var id = this.id;
  // alert(id);
  $(".department").css("display", "none");
  $(".imagelink").css("display", "none");
  $("." + id).css("display", "block");
  $(".backbutton").attr("id", id);
  $(".backbutton").css("display", "block");
});

$(".backbutton").click(function() {
  var id = this.id;
  $(".department").css("display", "block");
  $(".imagelink").css("display", "block");
  $("." + id).css("display", "none");
  $(".backbutton").css("display", "none");
  $(".backbutton").attr("id", "");
});
