// Chrome Extension Hello content script
// Example extension that shows a banner
// Generated with chrome_extension_basic in 2024 by Your Name

(function() {
  const banner = document.createElement('div');
  banner.textContent = 'AGF generated extension active: chrome_extension_hello';
  banner.style.position = 'fixed';
  banner.style.bottom = '1rem';
  banner.style.right = '1rem';
  banner.style.padding = '0.75rem 1rem';
  banner.style.background = '#111';
  banner.style.color = '#fff';
  banner.style.zIndex = 9999;
  banner.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)';
  document.body.appendChild(banner);
  console.log('AGF extension says hello from Chrome Extension Hello');
})();
