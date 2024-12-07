barba.init({
  transitions: [{
    name: 'fade',
    leave(data) {
      return new Promise(resolve => {
        data.current.container.style.opacity = 0;
        setTimeout(resolve, 500); // Delay for fade-out effect
      });
    },
    enter(data) {
      data.next.container.style.opacity = 0;
      setTimeout(() => {
        data.next.container.style.opacity = 1;
      }, 10);
    }
  }]
});


$(document).ready(function() {
  $(".close-btn").click(function() {
      $(this).closest(".flash-message").fadeOut();
  });
});