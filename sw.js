const CACHE_NAME = 'crossfit-box-v2'; // CAMBIÉ LA VERSIÓN

const urlsToCache = [
  '/registro.html',
  '/manifest.json',
  '/static/icon-72.png',
  '/static/icon-96.png',
  '/static/icon-144.png',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

// Instalar
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
  self.skipWaiting(); // Fuerza la activación inmediata
});

// Activar - limpiar caché vieja
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  return self.clients.claim(); // Toma control inmediato
});

// Fetch
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});