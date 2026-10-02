/* Sizes the logical stage and fits it to the viewport. */
(function () {
  var p = new URLSearchParams(location.search);
  var W = parseInt(p.get('w') || '1080', 10);
  var H = parseInt(p.get('h') || '1920', 10);
  var root = document.documentElement;
  root.style.setProperty('--W', W + 'px');
  root.style.setProperty('--H', H + 'px');
  root.setAttribute('data-fmt', W === H ? 'square' : (H > W ? 'vertical' : 'wide'));
  if (p.get('guides') === '1') root.setAttribute('data-guides', '1');
  function fit() {
    var s = Math.min(innerWidth / W, innerHeight / H);
    root.style.setProperty('--S', s);
  }
  fit();
  addEventListener('resize', fit);
  window.STAGE = { W: W, H: H };
})();
