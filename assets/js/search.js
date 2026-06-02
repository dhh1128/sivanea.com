// Live full-text search for the homepage. Loads /search.json, builds a Lunr
// index in the browser, and filters as you type. With no JS (or before the
// index loads) the page just shows the normal Contents list — graceful.
(function () {
  var box = document.getElementById('search-box');
  var results = document.getElementById('search-results');
  var contents = document.getElementById('contents');
  if (!box || !results || !contents) return;

  var idx = null;
  var docs = {};

  fetch('/search.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      idx = lunr(function () {
        this.ref('url');
        this.field('title', { boost: 10 });
        this.field('content');
        var self = this;
        data.forEach(function (d) { self.add(d); docs[d.url] = d; });
      });
      if (box.value.trim()) render();   // in case the user typed before load
    })
    .catch(function () { box.placeholder = 'Search unavailable'; });

  box.addEventListener('input', render);

  function render() {
    var q = box.value.trim();
    if (!q || !idx) {
      results.innerHTML = '';
      results.hidden = true;
      contents.hidden = false;
      return;
    }
    contents.hidden = true;
    results.hidden = false;

    // Two clauses per term: a plain (stemmed) term so whole words match the
    // stemmed index (e.g. "castle" → "castl"), and a trailing-wildcard term so
    // prefixes match while you're still typing (e.g. "cast" → "castl…").
    var hits = idx.query(function (query) {
      q.toLowerCase().split(/\s+/).forEach(function (term) {
        if (!term) return;
        query.term(term);
        query.term(term, { wildcard: lunr.Query.wildcard.TRAILING });
      });
    });

    if (!hits.length) {
      results.innerHTML = '<li class="search-empty">No matches for “' +
        escapeHtml(q) + '”.</li>';
      return;
    }

    results.innerHTML = hits.slice(0, 40).map(function (h) {
      var d = docs[h.ref];
      var snip = snippet(d.content, q);
      return '<li><a href="' + d.url + '">' + escapeHtml(d.title) + '</a>' +
        (snip ? '<div class="search-snippet">' + snip + '</div>' : '') + '</li>';
    }).join('');
  }

  // First match of any query term, with ~70 chars of context on each side and
  // the matched term emphasized.
  function snippet(content, q) {
    if (!content) return '';
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    var lc = content.toLowerCase();
    var at = -1, hitTerm = '';
    terms.forEach(function (t) {
      var i = lc.indexOf(t);
      if (i !== -1 && (at === -1 || i < at)) { at = i; hitTerm = t; }
    });
    if (at === -1) return escapeHtml(content.slice(0, 140)) + '…';
    var start = Math.max(0, at - 70);
    var end = Math.min(content.length, at + hitTerm.length + 70);
    var pre = (start > 0 ? '…' : '') + content.slice(start, at);
    var mid = content.slice(at, at + hitTerm.length);
    var post = content.slice(at + hitTerm.length, end) + (end < content.length ? '…' : '');
    return escapeHtml(pre) + '<mark>' + escapeHtml(mid) + '</mark>' + escapeHtml(post);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
})();
