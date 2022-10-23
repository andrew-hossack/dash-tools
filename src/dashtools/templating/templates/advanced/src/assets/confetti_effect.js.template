window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.my_clientside_library = {
  confetti_onclick: function (n_clicks) {
    confetti({
      particleCount: 100,
      startVelocity: 25,
      spread: 360,
      origin: {
        x: 0.5,
        // since they fall down, start a bit higher than random
        y: 0.3,
      },
    });
    // Reset confetti after 5 seconds
    setTimeout(() => {
      confetti.reset();
    }, 5000);
    return "foo doesnt matter";
  },
};
