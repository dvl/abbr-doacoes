
$(document).ready(function() {
  "use strict";

	$("#message2").fadeOut();

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
