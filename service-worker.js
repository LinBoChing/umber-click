
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('pwa-cache').then(function(cache) {
      return cache.addAll([
        './v180.html',
        './manifest.json'
      ]);
    })
  );
});
self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});
