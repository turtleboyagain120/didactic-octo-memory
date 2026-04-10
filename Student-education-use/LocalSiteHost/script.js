function loadSite() {
  const url = document.getElementById('url').value;
  if (!url) return alert('Enter URL!');
  // Local proxy endpoint
  document.getElementById('frame').src = '/proxy?url=' + encodeURIComponent(url);
}

