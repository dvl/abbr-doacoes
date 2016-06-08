$(document).ready(function() {
  function calculateSizes() {
    windowHeight = $(window).height();
    $("html").hasClass("ipad ios7") && (windowHeight -= 20);
    windowWidth = $(window).width();
    topnavHeight = parseInt($("body").css("paddingTop"), 10);
    viewportHeight = windowHeight - topnavHeight;
  }

  function calculateScroll() {
    bodyScroll = $(window).scrollTop()
  }

  var windowHeight = 600;
  var windowWidth = 1020;
  var topnavHeight = 50;
  var viewportHeight = 970;
  var bodyScroll = 0;
  calculateScroll();

  function a() {
    $("#nav_container").css("height", viewportHeight);
  }

  function n() {
    if ($(".case_header_container").length) {
      var a = $(document).scrollTop();
      a > 0 ? $(".case_header_container").addClass("fade") : $(".case_header_container").removeClass("fade")
    }
  }

  $ = jQuery.noConflict(), navigator.userAgent.match(/iPad;.*CPU.*OS 7_\d/i) && !window.navigator.standalone && $("html").addClass("ipad ios7"), $("body").addClass("doc-ready"), calculateSizes(), $("#menu_button").click(function () {
    $("body").hasClass("nav-active") ? ($("body").removeClass("nav-active"), $("#nav_container").removeClass("about_active"), $(".page_container").addClass("no-scale")) : ($("body").addClass("nav-active"), $(".page_container").removeClass("no-scale"))
  });

  $(document).click(function (a) {
    $(a.target).is("#nav_container *, #menu_button") || $("body").hasClass("nav-active") && (
      $("body").removeClass("nav-active"), $("#nav_container").removeClass("about_active"), $(".page_container").addClass("no-scale"))
  });

  $("#nav_about").click(function (a) {
    $("#nav_container").addClass("about_active");
  });

  $("#nav_about_close").click(function (a) {
    $("#nav_container").removeClass("about_active");
    $("#nav_container").removeClass("contact_active");
    $(".page_container").addClass("no-scale");
  })

  $("#nav_contact").click(function (a) {
    $("#nav_container").addClass("contact_active");
  });

  a();

  $(window).resize(function() {
    var windowHeight = $(window).height();
    topnavHeight = parseInt($("body").css("paddingTop"), 10);
    viewportHeight = windowHeight - topnavHeight;
    $("#nav_container").css("height", viewportHeight);
  });
});

$(document).ready(function($) {
  $.supersized({
    slideshow: 1,
    autoplay: 1,
    start_slide: 1,
    stop_loop: 0,
    random: 0,
    slide_interval: 2000,
    transition: 1,
    transition_speed: 1500,
    new_window: 1,
    pause_hover: 0,
    keyboard_nav: 1,
    performance:1,
    image_protect: 1,
    min_width: 0,
    min_height: 0,
    vertical_center: 1,
    horizontal_center: 1,
    fit_always: 0,
    fit_portrait: 1,
    fit_landscape: 0,
    slide_links: 'blank',
    thumb_links: 1,
    thumbnail_navigation: 0,
    slides: [
      {
        image: '/static/img/slider/1.jpg'
      },
      {
        image: '/static/img/slider/2.jpg'
      },
      {
        image: '/static/img/slider/3.jpg'
      }
    ],
    progress_bar: 1,
    mouse_scrub: 0
  });
});

function fbShare() {
  var winTop = (screen.height / 2) - (350 / 2),
    winLeft = (screen.width / 2) - (520 / 2);

  window.open('https://www.facebook.com/sharer/sharer.php?u=http%3A//www.abbr.org.br/', '', 'top='+winTop+', left='+winLeft+',width=520, height=350');
}

function twitterShare() {
  var winTop = (screen.height / 2) - (350 / 2),
    winLeft = (screen.width / 2) - (520 / 2);

  window.open('https://twitter.com/share?url=http%3A//www.abbr.org.br/', '', 'top='+winTop+', left='+winLeft+',width=720, height=550');
}
