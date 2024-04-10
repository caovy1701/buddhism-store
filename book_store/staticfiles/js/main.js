(function ($) {
	"use strict";

/*=============================================
	=    		 Preloader			      =
=============================================*/
    function preloader() {
        jQuery('.smart-page-loader').delay(0).fadeOut();
        jQuery('body:not(".elementor-editor-active")').removeClass('wp-smart-body');
    };

    $(window).on('load', function () {
        preloader();

    });



function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}
/*=============================================
	=    		Mobile Menu			      =
=============================================*/
//SubMenu Dropdown Toggle
if ($('.menu-area li.menu-item-has-children ul').length) {
	$('.menu-area .navigation li.menu-item-has-children').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

}


//Mobile Nav Hide Show
if ($('.mobile-menu').length) {

	var mobileMenuContent = $('.menu-area .main-menu').html();
	$('.mobile-menu .menu-box .menu-outer').append(mobileMenuContent);

	//Dropdown Button
	$('.mobile-menu li.menu-item-has-children .dropdown-btn').on('click', function () {
		$(this).toggleClass('open');
		$(this).prev('ul').slideToggle(500);
	});
	//Menu Toggle Btn
	$('.mobile-nav-toggler').on('click', function () {
		$('body').addClass('mobile-menu-visible');
	});

	//Menu Toggle Btn
	$('.menu-backdrop, .mobile-menu .close-btn').on('click', function () {
		$('body').removeClass('mobile-menu-visible');
	});
    }

    $('.socialclick').on('click', function () {
        $('.header-top-right').toggle(1000);
    });


    $('.click-two-header').on('click', function () {
        $('.show-two-header').toggle(1000);
    });
    $('.close-two').on('click', function () {
        $('.show-two-header').hide(1000);
    });


    $('.click-three-header').on('click', function () {
        $('.show-three-header').toggle(1000);
    });
    $('.close-three').on('click', function () {
        $('.show-three-header').hide(1000);
    });
    $('.click-four-header').on('click', function () {
        $('.show-four-header').toggle(1000);
    });
    $('.close-four').on('click', function () {
        $('.show-four-header').hide(1000);
    });



// Elements Animation
  $( document ).ready(function() {
    new WOW().init()
    if ($('.wow').length) {
        var wow = new WOW(
            {
                boxClass: 'wow',      // animated element css class (default is wow)
                animateClass: 'animated', // animation css class (default is animated)
                offset: 0,          // distance to the element when triggering the animation (default is 0)
                mobile: false,       // trigger animations on mobile devices (default is true)
                live: true       // act on asynchronously loaded content (default is true)
            }
        );
        wow.init();
    }
    });

const hide = document.querySelector(".icons");
      window.addEventListener("load", () => {
        document.body.classList.remove("preload");
      });

      document.addEventListener("DOMContentLoaded", () => {
        const nav = document.querySelector(".nav");

        document.querySelector("#btnNav").addEventListener("click", () => {
          nav.classList.add("nav--open");
        });

        hide.addEventListener("click", () => {
          nav.classList.remove("nav--open");
        });

        document
          .querySelector(".nav__overlay")
          .addEventListener("click", () => {
            nav.classList.remove("nav--open");
          });
      });

    //let url = window.location.href;
    //$('.navigation li a').each(function () {
    //    if (this.href === url) {
    //        $(this).closest('li').addClass('active');
    //    }
    //})
    /*=============================================
	=     Background Data Images     =
=============================================*/
    var list = document.querySelectorAll("div[data-image]");

    for (var i = 0; i < list.length; i++) {
        var url = list[i].getAttribute('data-image');
        list[i].style.backgroundImage = "url('" + url + "')";
    }
/*=============================================
	=     Menu sticky & Scroll to top      =
=============================================*/
$(window).on('scroll', function () {
	var scroll = $(window).scrollTop();
	if (scroll < 245) {
		$("#sticky-header").removeClass("sticky-menu");
		$('.scroll-to-target').removeClass('open');

	} else {
		$("#sticky-header").addClass("sticky-menu");
		$('.scroll-to-target').addClass('open');
	}
});


/*=============================================
	=    		 Scroll Up  	         =
=============================================*/
if ($('.scroll-to-target').length) {
  $(".scroll-to-target").on('click', function () {
    var target = $(this).attr('data-target');
    // animate
    $('html, body').animate({
      scrollTop: $(target).offset().top
    }, 1000);

  });
}
    
    var swiper = new Swiper(".mySwiper", {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        spaceBetween: 0,
        parallax: true,
        autoplay: 400,
        speed: 800,
        autoplayDisableOnInteraction: false,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });
/*=============================================
	=           Data Background             =
=============================================*/
$("[data-background]").each(function () {
	$(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
})


/*=============================================
	=    		Button Effect  	         =
=============================================*/
$('.btn').on('mouseenter', function (e) {
	var parentOffset = $(this).offset(),
		relX = e.pageX - parentOffset.left,
		relY = e.pageY - parentOffset.top;
	$(this).find('span').css({ top: relY, left: relX })
}).on('mouseout', function (e) {
	var parentOffset = $(this).offset(),
		relX = e.pageX - parentOffset.left,
		relY = e.pageY - parentOffset.top;
	$(this).find('span').css({ top: relY, left: relX })
});

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("actives");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}
    /*=============================================
	=    		VideoPlay 	         =
=============================================*/
    $('.popup-youtube').magnificPopup({
        type: 'iframe'
    });
        $('#demoslide3').owlCarousel({
loop: true,
autoplay: true,
autoPlaySpeed: 5000,
autoplayTimeout: 5000,
autoplayHoverPause: false,
margin: 25,
responsiveClass: true,
navText: ["<img src='static/images/left-arrow.png'/>", "<img src='static/images/right-arrow.png'/>"],
responsive: {
0: {
items: 1,
nav: true
},
600: {
items: 2,
nav: false
},
1000: {
items: 2,
autoplay: true,
autoplayHoverPause: false,
nav: true,
dots: false,
loop: true
}
}
})

        $('#demoslide4').owlCarousel({
            loop: false,
autoplay: true,
autoPlaySpeed: 5000,
autoplayTimeout: 5000,
autoplayHoverPause: false,
margin: 25,
responsiveClass: true,
navText: ["<img src='static/images/left-arrow.png'/>", "<img src='static/images/right-arrow.png'/>"],
responsive: {
0: {
items: 1,
nav: true
},
600: {
items: 2,
nav: false
},
1000: {
items: 4,
autoplay: true,
autoplayHoverPause: false,
nav: true,
dots: false,
loop: true
}
}
})

          $('#demoslide2').owlCarousel({
loop: true,
autoplay: true,
autoPlaySpeed: 5000,
autoplayTimeout: 5000,
autoplayHoverPause: false,
margin: 25,
responsiveClass: true,
navText: ["<img src='static/images/left-arrow.png'/>", "<img src='static/images/right-arrow.png'/>"],
responsive: {
0: {
items: 1,
nav: true
},
600: {
items: 2,
nav: false
},
1000: {
items: 3,
autoplay: true,
autoplayHoverPause: false,
nav: true,
dots: false,
loop: true
}
}
})
           $('#demoslide1').owlCarousel({
loop: true,
autoplay: true,
autoPlaySpeed: 5000,
autoplayTimeout: 5000,
autoplayHoverPause: false,
margin: 25,
responsiveClass: true,
navText: ["<img src='static/images/left-arrow1.png'/>", "<img src='static/images/right-arrow (1).png'/>"],
responsive: {
0: {
items: 1,
nav: true
},
600: {
items: 2,
nav: false
},
1000: {
items: 3,
autoplay: true,
autoplayHoverPause: false,
nav: true,
dots: false,
loop: true
}
}
})

    


/*=============================================
	=    		testmonial-4 	         =
=============================================*/
    $('.owl-demo5').owlCarousel({
        loop: true,
        autoplay: true,
        autoPlaySpeed: 5000,
        autoplayTimeout: 5000,
        autoplayHoverPause: false,
        margin: 25,
        responsiveClass: true,
        navText: ["<img src='static/images/left-arrow-small.png'/>", "<img src='static/images/right-arrow-small.png'/>"],
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            600: {
                items: 2,
                nav: false
            },
            1000: {
                items: 4,
                autoplay: true,
                autoplayHoverPause: false,
                nav: true,
                dots: false,
                loop: true
            }
        }
    })


    /*=============================================
	=    		testmonial-2 	         =
=============================================*/
    $('.owl-demo2').owlCarousel({
        loop: true,
        autoplay: true,
        autoPlaySpeed: 5000,
        autoplayTimeout: 5000,
        autoplayHoverPause: false,
        margin: 25,
        responsiveClass: true,
        navText: ["<img src='static/images/left-arrow-small.png'/>", "<img src='static/images/right-arrow-small.png'/>"],
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            600: {
                items: 1,
                nav: false
            },
            1000: {
                items: 1,
                autoplay: true,
                autoplayHoverPause: false,
                nav: true,
                dots: false,
                loop: true
            }
        }
    })
        /*=============================================
	=    		FAQ 	         =
=============================================*/
    $(".set > a").on("click", function () {
        if ($(this).hasClass("active")) {
            $(this).removeClass("active");
            $(this)
                .siblings(".content")
                .slideUp(200);
            $(".set > a i")
                .removeClass("fa-minus")
                .addClass("fa-plus");
        } else {
            $(".set > a i")
                .removeClass("fa-minus")
                .addClass("fa-plus");
            $(this)
                .find("i")
                .removeClass("fa-plus")
                .addClass("fa-minus");
            $(".set > a").removeClass("active");
            $(this).addClass("active");
            $(".content").slideUp(200);
            $(this)
                .siblings(".content")
                .slideDown(200);
        }
    })
    $('.service-carousel').owlCarousel({
        loop: true,
        margin: 0,
        fluidSpeed: true,
        smartSpeed: 2000,
        responsiveClass: true,
        dots: false,
        navText: ["<span class='icon icon-arrow-left'></span>", "<span class='icon icon-arrow-right'></span>"],
        nav: true,
        autoplay: true,
        autoplaySpeed: 2000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1,
            },
            400: {
                items: 1,
            },
            600: {
                items: 1,
            },
            1000: {
                items: 1,
            },
            1920: {
                items: 1
            }
        }

    });
    $('.main-carousel').owlCarousel({         
        loop: true,
        margin: 40,
        fluidSpeed: true,
        smartSpeed: 3000,
        responsiveClass: true,
        dots: false,
        navText: ['', ''],
        nav: true,
        autoplay: true,
        autoplaySpeed: 3000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1,
            },
            400: {
                items: 1,
            },
            600: {
                items: 3,
            },
            1000: {
                items: 4,
            },
            1920: {
                items: 6
            }
        }
         
    });


})(jQuery);