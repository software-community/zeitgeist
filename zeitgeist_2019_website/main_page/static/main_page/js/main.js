(function ($) {
  "use strict";

  // Scrollspy
  $("body").scrollspy({
    target: "#nav",
    offset: $(window).height() / 2,
  });

  // Mobile nav toggle
  $(".navbar-toggle").on("click", function () {
    $(".main-nav").toggleClass("open");
  });

  // Fixed nav
  $(window).on("scroll", function () {
    var wScroll = $(this).scrollTop();
    wScroll > 50
      ? $("#header").addClass("fixed-navbar")
      : $("#header").removeClass("fixed-navbar");
  });

  // Smooth scroll
  $(".main-nav a[href^='#']").on("click", function (e) {
    e.preventDefault();
    var hash = this.hash;
    $("html, body").animate(
      {
        scrollTop: $(this.hash).offset().top,
      },
      800
    );
  });

  // Section title animation
  $(".section-title").each(function () {
    var $this = $(this);
    $this.find(".title > span").each(function (i) {
      var $span = $(this);
      var animated = new Waypoint({
        element: $this,
        handler: function () {
          setTimeout(function () {
            $span.addClass("appear");
          }, i * 250);
          this.destroy();
        },
        offset: "95%",
      });
    });
  });

  // Galery Owl
  $("#galery-owl").owlCarousel({
    items: 1,
    loop: true,
    margin: 0,
    dots: false,
    nav: true,
    navText: [
      '<i class="fa fa-angle-left"></i>',
      '<i class="fa fa-angle-right"></i>',
    ],
    autoplay: true,
    autoplaySpeed: 500,
    navSpeed: 500,
    responsive: {
      0: {
        stagePadding: 0,
      },
      768: {
        stagePadding: 120,
      },
    },
  });

  // Parallax Background
  $.stellar({
    horizontalScrolling: false,
    responsive: true,
  });

  // CountTo
  $(".counter").each(function () {
    var $this = $(this);
    var counter = new Waypoint({
      element: $this,
      handler: function () {
        $this.countTo();
      },
      offset: "95%",
    });
  });
})(jQuery);

$(".black-f-but").hover(function () {
  $(".t-shirt").each(function () {
    $(this).css("opacity", "0");
  });
  $(".black-f").css("opacity", "1");
});
$(".black-b-but").hover(function () {
  $(".t-shirt").each(function () {
    $(this).css("opacity", "0");
  });
  $(".black-b").css("opacity", "1");
});
$(".blue-f-but").hover(function () {
  $(".t-shirt").each(function () {
    $(this).css("opacity", "0");
  });
  $(".blue-f").css("opacity", "1");
});
$(".blue-b-but").hover(function () {
  $(".t-shirt").each(function () {
    $(this).css("opacity", "0");
  });
  $(".blue-b").css("opacity", "1");
});

// Stage
cur_pos = 0;
auto_scroll = false;
window.addEventListener("scroll", function (e) {
  if (
    this.scrollY > cur_pos &&
    this.scrollY + screen.height >= $(".stage").offset().top &&
    this.scrollY <= $(".stage").offset().top
  ) {
    if (auto_scroll == false) {
      auto_scroll = true;
      window.scroll({
        top: $(".stage").offset().top,
        behavior: "smooth",
      });
    }
    $(".transparent-navbar").css("opacity", "0");
  } else if (
    this.scrollY < cur_pos &&
    this.scrollY >= $(".stage").offset().top &&
    this.scrollY <= $(".stage").offset().top + screen.height
  ) {
    if (auto_scroll == false) {
      auto_scroll = true;
      window.scroll({
        top: $(".stage").offset().top,
        behavior: "smooth",
        speed: 5000,
      });
    }
    $(".transparent-navbar").css("opacity", "0");
  } else if (
    this.scrollY < $(".stage").offset().top - 30 ||
    this.scrollY > $(".stage").offset().top + $(".stage").height()
  ) {
    $(".transparent-navbar").css("opacity", "1");
  }
  if (this.scrollY == $(".stage").offset().top) {
    auto_scroll = false;
  }

  cur_pos = this.scrollY;
});

function is_touch_device() {
  try {
    document.createEvent("TouchEvent");
    touch = true;
  } catch (e) {
    window.addEventListener("mousemove", function (e) {
      $(".stage-back").css(
        "transform",
        "translateX(" +
          (e.clientX.toString() / screen.width) * 50 +
          "px)" +
          " " +
          "translateY(" +
          (e.clientY.toString() / screen.height) * 50 +
          "px)"
      );
      $(".stage-front").css(
        "transform",
        "translateX(" +
          (e.clientX.toString() / screen.width) * 100 +
          "px)" +
          " " +
          "translateY(" +
          (e.clientY.toString() / screen.height) * 100 +
          "px)"
      );
    });
  }
}
is_touch_device();