// Service Worker - Versión sin caché problemático
const CACHE_NAME = 'crossfit-box-v3';

// No pre-cacheamos nada para evitar problemas
const urlsToCache = [];

self.addEventListener('install', event => {
  // Forzar activación inmediata
  self.skipWaiting();
  console.log('Service Worker instalado v3');
});

self.addEventListener('activate', event => {
  // Limpiar todo el caché viejo
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          console.log('Eliminando caché:', cache);
          return caches.delete(cache);
        })
      );
    })
  );
  self.clients.claim();
  console.log('Service Worker activado v3 - Caché limpiado');
});

// No interceptar fetch - ir directamente a la red
self.addEventListener('fetch', event => {
  // Simplemente ir a la red sin caché
  event.respondWith(fetch(event.request).catch(error => {
    console.error('Fetch falló:', error);
    return new Response('Error de conexión', { status: 500 });
  }));
});