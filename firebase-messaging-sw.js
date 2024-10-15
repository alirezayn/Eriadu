
const firebaseConfig = {
  apiKey: "AIzaSyCtnmFMYWIq1XbywVNq1UY1dVU1ZlpuXjQ",
  authDomain: "eriadu-project.firebaseapp.com",
  projectId: "eriadu-project",
  storageBucket: "eriadu-project.appspot.com",
  messagingSenderId: "361147699641",
  appId: "1:361147699641:web:52ee6a7926cb82425a6668",
  measurementId: "G-NZLLQ9WWBN",
};

// Initialize Firebase in Service Worker
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Background message handler
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/firebase-logo.png',
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
