/* GMK Media — deterministic ad timeline engine.
   Every visual state is a pure function of time, so a frame-stepping
   renderer and the live preview produce byte-identical output.
   No CSS transitions or keyframes anywhere: they are wall-clock bound. */
(function (global) {
  'use strict';

  var EASE = {
    linear: function (t) { return t; },
    out:    function (t) { return 1 - Math.pow(1 - t, 3); },
    inOut:  function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; },
    back:   function (t) { var c = 1.70158, u = t - 1; return 1 + (c + 1) * u * u * u + c * u * u; }
  };

  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function num(v, d) { var n = parseFloat(v); return isNaN(n) ? d : n; }

  function collect(root) {
    var scenes = [], items = [];

    Array.prototype.forEach.call(root.querySelectorAll('[data-scene]'), function (el) {
      scenes.push({
        el: el,
        t0: num(el.dataset.in, 0),
        t1: el.dataset.out === undefined ? null : num(el.dataset.out, null)
      });
    });

    Array.prototype.forEach.call(root.querySelectorAll('[data-anim]'), function (el) {
      var scene = el.closest('[data-scene]');
      var base  = scene ? num(scene.dataset.in, 0) : 0;
      var t0    = el.dataset.at !== undefined ? base + num(el.dataset.at, 0) : num(el.dataset.in, base);
      var out   = el.dataset.out !== undefined ? base + num(el.dataset.out, 0) : null;
      items.push({
        el: el,
        anim: el.dataset.anim,
        t0: t0,
        dur: num(el.dataset.dur, 0.55),
        out: out,
        outDur: num(el.dataset.outdur, 0.3),
        ease: EASE[el.dataset.ease] || EASE.out,
        amt: num(el.dataset.amt, 1),
        to: num(el.dataset.to, 100),
        from: num(el.dataset.from, 0),
        suffix: el.dataset.suffix || ''
      });
    });

    return { scenes: scenes, items: items };
  }

  function applyItem(it, t) {
    var el = it.el;
    var p  = it.ease(clamp01((t - it.t0) / Math.max(it.dur, 0.0001)));
    var fade = 1;
    if (it.out !== null) fade = 1 - clamp01((t - it.out) / Math.max(it.outDur, 0.0001));

    switch (it.anim) {
      case 'fade':
        el.style.opacity = p * fade;
        break;
      case 'rise':
        el.style.opacity = p * fade;
        el.style.transform = 'translate3d(0,' + ((1 - p) * 54 * it.amt).toFixed(3) + 'px,0)';
        break;
      case 'drop':
        el.style.opacity = p * fade;
        el.style.transform = 'translate3d(0,' + ((p - 1) * 54 * it.amt).toFixed(3) + 'px,0)';
        break;
      case 'slideL':
        el.style.opacity = p * fade;
        el.style.transform = 'translate3d(' + ((1 - p) * 70 * it.amt).toFixed(3) + 'px,0,0)';
        break;
      case 'slideR':
        el.style.opacity = p * fade;
        el.style.transform = 'translate3d(' + ((p - 1) * 70 * it.amt).toFixed(3) + 'px,0,0)';
        break;
      case 'pop':
        el.style.opacity = p * fade;
        el.style.transform = 'scale(' + (0.9 + 0.1 * p).toFixed(4) + ')';
        break;
      case 'wipe':
        el.style.opacity = fade;
        el.style.clipPath = 'inset(0 ' + ((1 - p) * 100).toFixed(3) + '% 0 0)';
        break;
      case 'wipeUp':
        el.style.opacity = fade;
        el.style.clipPath = 'inset(' + ((1 - p) * 100).toFixed(3) + '% 0 0 0)';
        break;
      case 'bar':
        el.style.opacity = fade;
        el.style.width = (p * it.to).toFixed(3) + '%';
        break;
      case 'count':
        el.style.opacity = fade;
        el.textContent = Math.round(it.from + (it.to - it.from) * p) + it.suffix;
        break;
      case 'hold':
        el.style.opacity = fade;
        break;
      default:
        el.style.opacity = p * fade;
    }
  }

  function Engine(opts) {
    this.duration = opts.duration;
    this.root = opts.root || document.body;
    var c = collect(this.root);
    this.scenes = c.scenes;
    this.items = c.items;
    this.onFrame = opts.onFrame || null;
  }

  Engine.prototype.seek = function (t) {
    t = Math.max(0, Math.min(t, this.duration));
    for (var i = 0; i < this.scenes.length; i++) {
      var s = this.scenes[i];
      var live = t >= s.t0 - 0.0005 && (s.t1 === null || t < s.t1);
      s.el.style.display = live ? '' : 'none';
    }
    for (var j = 0; j < this.items.length; j++) applyItem(this.items[j], t);
    if (this.onFrame) this.onFrame(t);
    this.t = t;
  };

  Engine.prototype.play = function () {
    var self = this, start = null;
    this.playing = true;
    function step(ts) {
      if (!self.playing) return;
      if (start === null) start = ts;
      var t = (ts - start) / 1000;
      if (t >= self.duration) { self.seek(self.duration); start = ts; t = 0; }
      self.seek(t);
      global.requestAnimationFrame(step);
    }
    global.requestAnimationFrame(step);
  };

  Engine.prototype.pause = function () { this.playing = false; };

  /* Boot. Render mode (?render=1) never auto-plays: the renderer seeks. */
  global.AdEngine = {
    EASE: EASE,
    mount: function (opts) {
      var params = new URLSearchParams(global.location.search);
      var engine = new Engine(opts);
      var renderMode = params.get('render') === '1';

      global.AD = {
        duration: opts.duration,
        seek: function (t) { engine.seek(t); },
        engine: engine,
        ready: false
      };

      function start() {
        engine.seek(0);
        global.AD.ready = true;
        document.documentElement.setAttribute('data-ad-ready', '1');
        if (renderMode) {
          document.documentElement.setAttribute('data-render', '1');
        } else {
          engine.play();
          document.addEventListener('keydown', function (e) {
            if (e.key === 'r' || e.key === 'R') { engine.pause(); engine.play(); }
            if (e.key === ' ') { e.preventDefault(); engine.playing ? engine.pause() : engine.play(); }
          });
          document.addEventListener('click', function () { engine.pause(); engine.play(); });
        }
      }

      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(start).catch(start);
      } else {
        start();
      }
      return engine;
    }
  };
})(window);
