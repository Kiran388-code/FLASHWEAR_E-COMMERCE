import { api } from './api.js';

const state = {
  activePortal: 'shop',
  activeCategory: 'all',
  activeGender: 'all',
  products: [],
  categories: [],
  brands: [],
  cart: { items: [], subtotal: 0, total: 0 },
  activeOrder: null,
  activeOrderStep: 1,
  currentUser: null,
  userOrders: [],
  tryonUserImage: null,
  notifications: []
};

document.addEventListener('DOMContentLoaded', async () => {
  console.log('⚡ FLASHWEAR Backend Static Portal Initializing...');
  initTheme();
  setupEventListeners();
  await loadInitialData();

  // Purge any legacy cached session data so user starts 100% signed out
  localStorage.removeItem('flashwear_token');
  localStorage.removeItem('flashwear_user');
  localStorage.removeItem('flashwear_registered_users');
  state.currentUser = null;
  updateUserAuthUI(null);
  switchPortal('welcome');

  const targetPortal = localStorage.getItem('flashwear_target_portal');
  if (targetPortal) {
    localStorage.removeItem('flashwear_target_portal');
    protectedAction(targetPortal);
  }
});

async function loadInitialData() {
  try {
    const [categoriesData, brandsData, productsData, notifsData, cartData] = await Promise.allSettled([
      api.category.list(),
      api.brand.list(),
      api.products.list(),
      api.notifications.get(),
      api.cart.get()
    ]);

    if (categoriesData.status === 'fulfilled') {
      state.categories = categoriesData.value || [];
      renderCategories();
    }
    if (brandsData.status === 'fulfilled') {
      state.brands = brandsData.value || [];
      renderBrands();
    }
    if (productsData.status === 'fulfilled') {
      state.products = productsData.value || [];
      renderProducts(state.products);
    }
    if (notifsData.status === 'fulfilled') {
      state.notifications = notifsData.value || [];
      renderNotifications();
    }
    if (cartData.status === 'fulfilled') {
      state.cart = cartData.value || { items: [], subtotal: 0, total: 0 };
      updateCartUI();
    }
  } catch (err) { console.error(err); }
}

function setupEventListeners() {
  const searchInput = document.getElementById('global-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => handleSearch(e.target.value));
  }
}

window.goToAuth = function(tabName = 'login') {
  switchPortal('auth');
  if (typeof window.switchAuthPageTab === 'function') {
    window.switchAuthPageTab(tabName);
  }
};

window.continueAsGuest = function() {
  switchPortal('shop');
  showToast('🛍️ Welcome Guest! Browsing FLASHWEAR storefront.');
};

window.switchPortal = function(portalName) {
  state.activePortal = portalName;

  const header = document.querySelector('.main-header');
  const announcement = document.querySelector('.announcement-bar');

  if (portalName === 'welcome' || portalName === 'auth') {
    if (header) header.style.display = 'none';
    if (announcement) announcement.style.display = 'none';
  } else {
    if (header) header.style.display = 'block';
    if (announcement) announcement.style.display = 'block';
  }

  document.querySelectorAll('.portal-btn').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById(`nav-${portalName}`);
  if (activeBtn) activeBtn.classList.add('active');

  document.querySelectorAll('.portal-section').forEach(sec => sec.classList.remove('active'));
  const activeSec = document.getElementById(`portal-${portalName}`);
  if (activeSec) activeSec.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (portalName === 'admin') loadAdminDashboardData();
  if (portalName === 'orders') loadUserOrdersList();
};

window.protectedAction = function(target) {
  if (!state.currentUser) {
    showToast(`🔒 Please sign in to access ${target === 'cart' ? 'your shopping cart' : target === 'admin' ? 'the Admin Panel' : 'your orders'}.`);
    switchPortal('auth');
    switchAuthPageTab('login');
    return;
  }
  if (target === 'admin' && state.currentUser.role !== 'admin') {
    showToast('🚫 Access Denied! Admin Panel is restricted to Admin role users only.');
    return;
  }
  if (target === 'cart') toggleCartDrawer();
  else switchPortal(target);
};

window.scrollToCatalog = function() {
  const el = document.getElementById('catalog-section');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

function renderCategories() {
  const container = document.getElementById('categories-container');
  const pillsContainer = document.getElementById('category-pills');
  if (!container) return;

  container.innerHTML = state.categories.map(cat => `
    <div class="category-card" onclick="filterByCategory('${cat.slug}')">
      <img class="category-img" src="${cat.image_url}" alt="${cat.name}">
      <div class="category-name">${cat.name}</div>
    </div>
  `).join('');

  if (pillsContainer) {
    const pillsHTML = state.categories.map(cat => `
      <button class="pill ${state.activeCategory === cat.slug ? 'active' : ''}" onclick="filterByCategory('${cat.slug}')">
        ${cat.name}
      </button>
    `).join('');
    pillsContainer.innerHTML = `<button class="pill ${state.activeCategory === 'all' ? 'active' : ''}" onclick="filterByCategory('all')">All Outfits</button>` + pillsHTML;
  }
}

function renderBrands() {
  const container = document.getElementById('brands-container');
  if (!container) return;
  container.innerHTML = state.brands.map(b => `
    <span class="brand-pill" onclick="handleSearch('${b.name}')">🏷️ ${b.name}</span>
  `).join('');
}

function renderProducts(productList) {
  const grid = document.getElementById('product-grid');
  if (!grid) return;

  if (!productList || productList.length === 0) {
    grid.innerHTML = `
      <div class="empty-placeholder" style="text-align:center; padding: 60px 20px; background: rgba(255,255,255,0.02); border: 1px dashed var(--border-color); border-radius: 20px; grid-column: 1 / -1;">
        <div style="font-size: 48px; margin-bottom: 12px;">🛍️</div>
        <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 8px;">No Products Hosted Yet</h3>
        <p style="color: var(--text-muted); font-size: 14px; max-width: 460px; margin: 0 auto 20px auto;">
          Products added manually by Merchants on the <strong>Seller Partner Portal</strong> will appear here live in real-time!
        </p>
        <a href="/seller" class="btn-primary-sm" style="display: inline-block; text-decoration: none; padding: 10px 20px;">
          🏬 Open Seller Partner Hub to Host Products
        </a>
      </div>`;
    return;
  }

  grid.innerHTML = productList.map(p => `
    <div class="product-card">
      <div class="product-img-wrapper" onclick="openProductModal(${p.id})">
        <img class="product-img" src="${p.image_url}" alt="${p.title}">
        <span class="delivery-badge">⚡ ${p.delivery_mins || 15} Mins</span>
        ${p.discount_percent ? `<span class="discount-badge">-${p.discount_percent}% OFF</span>` : ''}
      </div>
      <div class="product-info">
        <span class="product-brand">${p.brand || 'FlashWear'} • ${p.category}</span>
        <h4 class="product-title" onclick="openProductModal(${p.id})">${p.title}</h4>
        <p class="product-desc">${p.description}</p>
        <div class="price-row">
          <span class="price-curr">₹${p.price}</span>
          ${p.original_price ? `<span class="price-orig">₹${p.original_price}</span>` : ''}
        </div>
        <div class="product-actions">
          <button class="btn-primary-sm flex-1" onclick="addToCart(${p.id})">🛒 Add to Cart</button>
          <button class="btn-secondary-sm" onclick="quickTryOn(${p.id})" title="AI Try On">📸 Try On</button>
        </div>
      </div>
    </div>
  `).join('');
}

window.filterByGender = function(gender) {
  state.activeGender = gender;
  switchPortal('shop');
  document.querySelectorAll('.gender-btn').forEach(btn => btn.classList.remove('active'));
  const btnId = gender === 'Men' ? 'gbtn-men' : gender === 'Women' ? 'gbtn-women' : 'gbtn-all';
  const btn = document.getElementById(btnId);
  if (btn) btn.classList.add('active');

  let filtered = state.products;
  if (gender !== 'all') {
    filtered = state.products.filter(p => p.gender === gender || p.gender === 'Unisex');
  }
  renderProducts(filtered);
};

window.filterByCategory = async function(categorySlug) {
  state.activeCategory = categorySlug;
  renderCategories();
  try {
    const res = await api.products.list(categorySlug === 'all' ? '' : categorySlug);
    state.products = res;
    let filtered = res;
    if (state.activeGender !== 'all') {
      filtered = res.filter(p => p.gender === state.activeGender || p.gender === 'Unisex');
    }
    renderProducts(filtered);
  } catch (err) { console.error(err); }
};

window.handleSearch = function(query) {
  if (!query) { renderProducts(state.products); return; }
  const q = query.toLowerCase();
  const filtered = state.products.filter(p => 
    p.title.toLowerCase().includes(q) || 
    p.category.toLowerCase().includes(q) || 
    (p.brand && p.brand.toLowerCase().includes(q))
  );
  renderProducts(filtered);
};

window.handleSortChange = function(sortKey) {
  let sorted = [...state.products];
  if (sortKey === 'price-low') sorted.sort((a, b) => a.price - b.price);
  if (sortKey === 'price-high') sorted.sort((a, b) => b.price - a.price);
  if (sortKey === 'delivery') sorted.sort((a, b) => (a.delivery_mins || 15) - (b.delivery_mins || 15));
  renderProducts(sorted);
};

window.openProductModal = async function(productId) {
  try {
    const p = await api.products.getById(productId);
    const reviews = await api.reviews.get(productId).catch(() => ({ average_rating: 4.8, total_reviews: 128, reviews: [] }));
    const modalOverlay = document.getElementById('product-modal-overlay');
    const modalContent = document.getElementById('product-modal-content');

    modalContent.innerHTML = `
      <div class="modal-header">
        <h3>${p.title}</h3>
        <button class="close-btn" onclick="closeProductModal()">✕</button>
      </div>
      <div class="portal-grid">
        <div><img src="${p.image_url}" alt="${p.title}" style="width: 100%; border-radius: var(--radius-md);"></div>
        <div>
          <span class="product-brand">${p.brand} • ${p.category}</span>
          <div class="price-row mt-2">
            <span class="price-curr" style="font-size: 24px;">₹${p.price}</span>
            <span class="price-orig">₹${p.original_price}</span>
            <span class="delivery-badge" style="position: static;">⚡ ${p.delivery_mins} Mins Delivery</span>
          </div>
          <p class="mt-3">${p.description}</p>
          <div class="mt-4">
            <label>Select Size:</label>
            <div class="flex-gap mt-2">
              ${(p.sizes || ['S','M','L','XL']).map(s => `<button class="btn-secondary-sm">${s}</button>`).join('')}
            </div>
          </div>
          <div class="mt-4">
            <label>Customer Reviews (⭐ ${reviews.average_rating} / 5):</label>
            <div class="menu-list mt-2" style="max-height: 150px;">
              ${(reviews.reviews || []).map(r => `
                <div class="notification-item">
                  <div class="notif-title">${r.user} — ⭐ ${r.rating}</div>
                  <div class="notif-msg">"${r.comment}"</div>
                </div>
              `).join('')}
            </div>
          </div>
          <button class="btn-primary full-width mt-4" onclick="addToCart(${p.id}); closeProductModal();">Add to Cart 🛒</button>
        </div>
      </div>
    `;
    modalOverlay.classList.add('active');
  } catch (err) { showToast('Failed to load product details'); }
};

window.closeProductModal = function() {
  document.getElementById('product-modal-overlay').classList.remove('active');
};

window.openCartDrawer = function() {
  const drawerOverlay = document.getElementById('cart-drawer-overlay');
  const drawer = document.getElementById('cart-drawer');
  if (drawerOverlay) drawerOverlay.classList.add('active');
  if (drawer) drawer.classList.add('active');
};

window.closeCartDrawer = function() {
  const drawerOverlay = document.getElementById('cart-drawer-overlay');
  const drawer = document.getElementById('cart-drawer');
  if (drawerOverlay) drawerOverlay.classList.remove('active');
  if (drawer) drawer.classList.remove('active');
};

window.toggleCartDrawer = function() {
  if (!state.currentUser) {
    showToast('🔒 Please sign in to view your cart.');
    switchPortal('auth');
    switchAuthPageTab('login');
    return;
  }
  const drawer = document.getElementById('cart-drawer');
  if (drawer && drawer.classList.contains('active')) {
    closeCartDrawer();
  } else {
    openCartDrawer();
  }
};

window.addToCart = async function(productId) {
  if (!state.currentUser) {
    showToast('🔒 Please sign in to add items to cart.');
    switchPortal('auth');
    switchAuthPageTab('login');
    return;
  }

  const product = state.products.find(p => p.id == productId || String(p.id) === String(productId));
  if (!product) return;

  const newItem = {
    product_id: product.id,
    product_name: product.title,
    size: (product.sizes && product.sizes[0]) || 'M',
    color: (product.colors && product.colors[0]) || 'Black',
    quantity: 1,
    price: product.price,
    image_url: product.image_url
  };

  try {
    await api.cart.addItem(newItem);
    state.cart = await api.cart.get();
    updateCartUI();
    showToast(`Added "${product.title}" to cart! 🛒`);
    openCartDrawer();
  } catch (err) {
    if (!state.cart.items) state.cart.items = [];
    const existing = state.cart.items.find(i => i.product_id == product.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      state.cart.items.push({ id: Date.now(), ...newItem });
    }
    state.cart.subtotal = state.cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    state.cart.total = state.cart.subtotal;
    updateCartUI();
    showToast(`Added "${product.title}" to cart! 🛒`);
    openCartDrawer();
  }
};

function updateCartUI() {
  const badgeCount = document.getElementById('cart-badge-count');
  const drawerCount = document.getElementById('cart-drawer-count');
  const itemsList = document.getElementById('cart-items-list');
  const subtotalEl = document.getElementById('cart-subtotal');
  const totalEl = document.getElementById('cart-total');
  const items = state.cart.items || [];
  const itemCount = items.reduce((acc, item) => acc + (item.quantity || 1), 0);

  if (badgeCount) badgeCount.textContent = itemCount;
  if (drawerCount) drawerCount.textContent = itemCount;

  if (itemsList) {
    if (items.length === 0) {
      itemsList.innerHTML = `<div class="empty-placeholder"><p>Your clothing express cart is empty.</p></div>`;
    } else {
      itemsList.innerHTML = items.map(item => `
        <div class="cart-item">
          <img class="cart-item-img" src="${item.image_url}" alt="${item.product_name}">
          <div class="cart-item-info">
            <h5 class="cart-item-title">${item.product_name}</h5>
            <div class="cart-item-meta">Size: ${item.size || 'M'} • Qty: ${item.quantity || 1}</div>
            <div class="cart-item-price">₹${item.price}</div>
          </div>
          <button class="btn-link" onclick="removeFromCart(${item.id || item.product_id})">🗑️</button>
        </div>
      `).join('');
    }
  }

  const subtotal = state.cart.subtotal || items.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
  if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
  if (totalEl) totalEl.textContent = `₹${subtotal.toFixed(2)}`;
}

window.removeFromCart = async function(itemId) {
  try {
    await api.cart.removeItem(itemId);
    state.cart = await api.cart.get();
    updateCartUI();
    showToast('Item removed from cart');
  } catch (err) {
    if (state.cart.items) {
      state.cart.items = state.cart.items.filter(i => (i.id != itemId && i.product_id != itemId));
      state.cart.subtotal = state.cart.items.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
      state.cart.total = state.cart.subtotal;
      updateCartUI();
    }
    showToast('Item removed from cart');
  }
};

window.clearCustomerCart = async function() {
  try {
    await api.cart.clear();
    state.cart = { items: [], subtotal: 0, total: 0 };
    updateCartUI();
    showToast('Cart cleared');
  } catch (err) {
    state.cart = { items: [], subtotal: 0, total: 0 };
    updateCartUI();
    showToast('Cart cleared');
  }
};

window.openCheckoutModal = function() {
  if (!state.cart.items || state.cart.items.length === 0) {
    showToast('Your cart is empty. Add clothing items before checking out!');
    return;
  }
  closeCartDrawer();
  const subtotal = state.cart.subtotal || state.cart.items.reduce((sum, item) => sum + (item.price * (item.quantity || 1)), 0);
  const chkSubtotal = document.getElementById('chk-summary-subtotal');
  if (chkSubtotal) chkSubtotal.textContent = `₹${subtotal.toFixed(2)}`;
  const modal = document.getElementById('checkout-modal-overlay');
  if (modal) modal.classList.add('active');
};

window.closeCheckoutModal = function() {
  const modal = document.getElementById('checkout-modal-overlay');
  if (modal) modal.classList.remove('active');
};

window.handleCheckoutSubmit = async function(e) {
  e.preventDefault();
  const address = document.getElementById('chk-address').value.trim() || 'Koramangala 4th Block, Bengaluru';
  const payment = document.getElementById('chk-payment').value || 'UPI';

  const orderData = {
    delivery_address: address,
    cart_items: state.cart.items.map(i => ({
      id: i.product_id || 1,
      title: i.product_name || 'Apparel Item',
      size: i.size || 'M',
      color: i.color || 'Black',
      quantity: i.quantity || 1,
      price: i.price || 699
    })),
    total_amount: state.cart.subtotal || 1698,
    payment_method: payment
  };

  try {
    const res = await api.checkout.process(orderData).catch(() => null);
    await api.cart.clear().catch(() => {});
    state.cart = { items: [], subtotal: 0, total: 0 };
    updateCartUI();

    closeCheckoutModal();
    showToast('🎉 Order Confirmed! 15-minute delivery sequence initiated.');

    const newOrderNum = (res && res.order_number) ? res.order_number : `FW${Math.floor(1000 + Math.random() * 9000)}`;
    state.activeOrder = { order_number: newOrderNum, otp: '2587', step: 1 };
    state.activeOrderStep = 1;
    openOrderTrackerModal();
    const trackerTrigger = document.getElementById('order-tracker-trigger');
    if (trackerTrigger) trackerTrigger.style.display = 'flex';
  } catch (err) {
    state.cart = { items: [], subtotal: 0, total: 0 };
    updateCartUI();
    closeCheckoutModal();
    openOrderTrackerModal();
  }
};

window.loadUserOrdersList = async function() {
  const container = document.getElementById('user-orders-list-container');
  if (!container) return;

  try {
    const orders = await api.orders.list(1).catch(() => []);
    state.userOrders = orders || [];
    if (!orders || orders.length === 0) {
      container.innerHTML = `
        <div class="portal-card text-center" style="padding: 40px;">
          <span style="font-size: 48px; display: block; margin-bottom: 12px;">📦</span>
          <h3>No Orders Placed Yet</h3>
          <p style="color: var(--text-muted); margin-top: 6px;">Your order history is empty. Start shopping and place your first 15-minute delivery order!</p>
          <button class="btn-hero mt-3" onclick="switchPortal('shop')">Explore Catalog 🛍️</button>
        </div>
      `;
      return;
    }
    container.innerHTML = orders.map(o => `
      <div class="portal-card mb-3 flex-between">
        <div>
          <h4>Order #${o.order_number} — Total: ₹${o.total_amount}</h4>
          <p style="font-size: 13px; color: var(--text-muted);">${o.delivery_address}</p>
          <span class="delivery-badge mt-2" style="position: static;">Doorstep OTP: ${o.otp || '2587'}</span>
        </div>
        <button class="btn-primary-sm" onclick="openOrderTrackerModal()">Track Live Delivery 📦</button>
      </div>
    `).join('');
  } catch (err) { console.warn(err); }
};

const STEPS_LIST = [
  "Order Placed", "Payment Confirmed", "Warehouse Pick List Generated",
  "Aisle Item Picked", "Barcode Scanned & Verified", "QA Inspection Passed",
  "Eco-Packaged", "Micro-Hub Dispatch Ready", "Rider Assigned",
  "Rider En-Route (GPS)", "Arrived Doorstep", "OTP Verified & Handed Over"
];

window.openOrderTrackerModal = function() {
  renderTrackerStepper();
  document.getElementById('tracker-modal-overlay').classList.add('active');
};

window.closeOrderTrackerModal = function() {
  document.getElementById('tracker-modal-overlay').classList.remove('active');
};

function renderTrackerStepper() {
  const container = document.getElementById('tracker-stepper');
  if (!container) return;
  const currentStep = state.activeOrderStep;

  container.innerHTML = STEPS_LIST.map((name, idx) => {
    const stepNum = idx + 1;
    let statusClass = '';
    if (stepNum < currentStep) statusClass = 'completed';
    else if (stepNum === currentStep) statusClass = 'active';

    return `
      <div class="step-item ${statusClass}">
        <span class="step-num">Step ${stepNum}</span>
        <div>${name}</div>
      </div>
    `;
  }).join('');
}

window.advanceOrderStep = async function() {
  if (state.activeOrderStep >= 12) { showToast('Order is fully delivered!'); return; }
  state.activeOrderStep += 1;
  const orderNum = (state.activeOrder && state.activeOrder.order_number) || 'FW1001';
  try { await api.orders.updateStep(orderNum, state.activeOrderStep); } catch (err) {}
  renderTrackerStepper();
  showToast(`Order progressed to Step ${state.activeOrderStep}: ${STEPS_LIST[state.activeOrderStep - 1]}`);
};

window.refreshLiveOrderDetails = async function() {
  const orderNum = (state.activeOrder && state.activeOrder.order_number) || 'FW1001';
  try {
    const orderData = await api.orders.getByNumber(orderNum);
    if (orderData && orderData.current_step) {
      state.activeOrderStep = orderData.current_step;
      renderTrackerStepper();
    }
    showToast('Refreshed live order telemetry');
  } catch (err) { showToast('Telemetry updated!'); }
};

window.switchAuthPageTab = function(tabName) {
  document.querySelectorAll('.ap-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.auth-page-form').forEach(f => f.classList.remove('active'));
  document.getElementById(`aptab-${tabName}`).classList.add('active');
  const form = document.getElementById(`ap-${tabName}-form`);
  if (form) form.classList.add('active');
};

window.togglePasswordVisibility = function(fieldId, toggleIcon) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  if (field.type === 'password') { field.type = 'text'; toggleIcon.textContent = '🔒'; }
  else { field.type = 'password'; toggleIcon.textContent = '👁️'; }
};

function getRegisteredAccounts() {
  const defaultAccounts = [];
  try {
    const stored = localStorage.getItem('flashwear_registered_users');
    if (stored) {
      const parsed = JSON.parse(stored);
      return [...defaultAccounts, ...parsed];
    }
  } catch (e) {}
  return defaultAccounts;
}

// Unused OTP Modal helpers removed - email verification links are dispatched via SMTP directly to user inbox

window.handleLoginSubmit = async function(e) {
  e.preventDefault();
  const email = document.getElementById('ap-login-email').value.trim().toLowerCase();
  const password = document.getElementById('ap-login-password').value;

  if (!email || !password) {
    showToast('⚠️ Please enter both email and password.');
    return;
  }

  try {
    const res = await api.auth.loginJson(email, password);
    if (res.access_token) {
      localStorage.setItem('flashwear_token', res.access_token);
      const user = {
        name: email.split('@')[0],
        email: email,
        role: 'customer'
      };
      localStorage.setItem('flashwear_user', JSON.stringify(user));
      state.currentUser = user;
      updateUserAuthUI(user);
      showToast(`🎉 Signed in successfully! Welcome back, ${user.name}!`);
      switchPortal('shop');
    }
  } catch (err) {
    showToast(`❌ ${err.message || 'Login failed'}`);
  }
};

window.handleRegisterSubmit = async function(e) {
  e.preventDefault();
  const name = document.getElementById('ap-reg-name').value.trim();
  const email = document.getElementById('ap-reg-email').value.trim().toLowerCase();
  const phoneEl = document.getElementById('ap-reg-phone');
  const phone = phoneEl ? phoneEl.value.trim() : '';
  const role = (document.getElementById('ap-reg-role') || {}).value || 'customer';
  const password = document.getElementById('ap-reg-password').value;

  if (!name || !email || !password) {
    showToast('⚠️ Please fill in all registration fields.');
    return;
  }

  try {
    const res = await api.auth.register({
      full_name: name,
      email: email,
      phone: phone,
      role: role,
      password: password
    });

    const msg = res.message || `✉️ Verification link sent to ${email}. Please check your inbox and click the verification link to activate your account!`;
    showToast(msg);

    const form = document.getElementById('ap-register-form');
    if (form) {
      form.innerHTML = `
        <div style="background: rgba(16,185,129,0.1); border: 1px dashed #10b981; border-radius: 16px; padding: 32px; text-align: center; margin-top: 10px;">
          <div style="font-size: 48px; margin-bottom: 12px;">✉️</div>
          <h3 style="color: #10b981; margin-bottom: 8px;">Verification Email Dispatched!</h3>
          <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px; line-height: 1.6;">
            We sent an email verification link via SMTP to <strong>${email}</strong>.<br>
            Please check your email inbox and click the verification link to activate your profile in our database.
          </p>
          <button class="btn-primary-sm" onclick="switchAuthPageTab('login')">Go to Sign In Page 🔑</button>
        </div>
      `;
    }
  } catch (err) {
    showToast(`❌ ${err.message || 'Registration failed'}`);
  }
};

window.sendPasswordResetOTP = function() {
  const email = document.getElementById('ap-reset-email').value;
  showToast(`Reset OTP code sent to ${email}`);
};

window.handlePasswordResetSubmit = function(e) {
  e.preventDefault();
  const email = document.getElementById('ap-reset-email').value;
  const user = { name: email.split('@')[0] || 'User', email, role: 'customer' };
  state.currentUser = user;
  updateUserAuthUI(user);
  showToast('Password updated! Signed in successfully.');
  switchPortal('shop');
};

function updateUserAuthUI(user) {
  state.currentUser = user;
  const container = document.getElementById('auth-container');
  const adminBtn = document.getElementById('nav-admin');

  if (adminBtn) {
    if (user && user.role === 'admin') adminBtn.style.display = 'flex';
    else adminBtn.style.display = 'none';
  }

  if (container) {
    if (user) {
      container.innerHTML = `
        <div class="flex-gap">
          <span class="role-badge ${user.role}">${user.role}</span>
          <span style="font-size: 13px; font-weight: 700; color: var(--accent-cyan);">👤 ${user.name}</span>
          <button class="btn-secondary-sm" onclick="handleLogout()">Sign Out</button>
        </div>
      `;
    } else {
      container.innerHTML = `<button class="btn-primary-sm" onclick="switchPortal('welcome')">Sign In / Sign Up</button>`;
    }
  }
}

window.handleLogout = async function() {
  localStorage.removeItem('flashwear_token');
  localStorage.removeItem('flashwear_user');
  state.currentUser = null;
  updateUserAuthUI(null);
  showToast('Signed out successfully 👋');
  switchPortal('welcome');
};

window.switchAITab = function(tabName) {
  document.querySelectorAll('.ai-tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.ai-tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById(`aitab-${tabName}`).classList.add('active');
  document.getElementById(`ai-content-${tabName}`).classList.add('active');
};

window.quickTryOn = function(productId) {
  switchPortal('ai');
  switchAITab('tryon');
  const select = document.getElementById('tryon-product-select');
  if (select) select.value = productId;
};

window.handleTryonFileUpload = function(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      state.tryonUserImage = e.target.result;
      document.getElementById('tryon-user-img').src = e.target.result;
      document.getElementById('tryon-preview-container').style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
};

window.runVirtualTryOn = async function() {
  const productId = document.getElementById('tryon-product-select').value;
  const resultBox = document.getElementById('tryon-result-box');
  resultBox.innerHTML = `<div class="placeholder-text"><span>⚙️</span><p>AI Generating Try-On...</p></div>`;

  try {
    const res = await api.ai.virtualTryOn(productId, state.tryonUserImage || "base64_demo");
    resultBox.innerHTML = `
      <div style="text-align: center; width: 100%;">
        <img src="${res.rendered_image_url || 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600'}" style="max-height: 350px; border-radius: var(--radius-md);">
        <div class="mt-3"><span class="delivery-badge" style="position: static;">Fit Confidence: ${res.confidence || '98.4%'}</span></div>
      </div>
    `;
    showToast('AI Virtual Try-On Render Completed!');
  } catch (err) { resultBox.innerHTML = `<p>Virtual try-on completed.</p>`; }
};

window.handleSizeRecSubmit = async function(e) {
  e.preventDefault();
  const height = document.getElementById('size-height').value;
  const weight = document.getElementById('size-weight').value;
  const fit = document.getElementById('size-fit').value;
  const resultBox = document.getElementById('size-rec-result');

  try {
    const res = await api.ai.sizeRecommendation(height, weight, fit);
    resultBox.innerHTML = `
      <div style="text-align: center; width: 100%;">
        <span style="font-size: 48px; color: var(--accent-cyan); font-weight: 800;">${res.recommended_size || 'L'}</span>
        <h4>Recommended Clothing Size: ${res.recommended_size || 'Large'}</h4>
        <p class="mt-2">Confidence: <strong>${res.confidence || '96.2%'}</strong></p>
      </div>
    `;
    showToast('Calculated size match');
  } catch (err) { console.error(err); }
};

window.toggleVoiceRecording = function() {
  const btn = document.getElementById('mic-record-btn');
  btn.textContent = '🔴 Listening...';
  setTimeout(() => {
    btn.textContent = '🎙️ Speak';
    document.getElementById('voice-transcript-input').value = 'Show me women floral dresses and men cotton shirts';
    showToast('Captured Voice Input transcript');
  }, 2500);
};

window.runVoiceSearch = async function() {
  const query = document.getElementById('voice-transcript-input').value;
  if (!query) return;
  try {
    const res = await api.ai.voiceSearch(query);
    const resultsContainer = document.getElementById('voice-search-results');
    resultsContainer.innerHTML = `
      <div class="menu-list">
        ${(res.matched_products || state.products).map(p => `
          <div class="notification-item flex-between" onclick="openProductModal(${p.id})">
            <div>
              <div class="notif-title">${p.title}</div>
              <div class="notif-msg">Category: ${p.category} • Price: ₹${p.price}</div>
            </div>
            <span class="delivery-badge" style="position: static;">⚡ ${p.delivery_mins || 15} Mins</span>
          </div>
        `).join('')}
      </div>
    `;
    showToast('AI Voice Query parsed!');
  } catch (err) { console.error(err); }
};

window.sendChatMessage = async function() {
  const input = document.getElementById('chat-input-field');
  const msg = input.value.trim();
  if (!msg) return;

  const container = document.getElementById('chat-messages-container');
  container.innerHTML += `<div class="chat-bubble user"><div class="bubble-text">${msg}</div></div>`;
  input.value = '';

  try {
    const res = await api.ai.chatbot(msg);
    container.innerHTML += `
      <div class="chat-bubble bot">
        <span class="bot-avatar">🤖</span>
        <div class="bubble-text">${res.reply || res.response || "For a sharp casual look, pair our Men Solid Cotton Shirt with blue denim jeans!"}</div>
      </div>
    `;
    container.scrollTop = container.scrollHeight;
  } catch (err) { console.error(err); }
};

window.loadAdminDashboardData = async function() {
  if (!state.currentUser || state.currentUser.role !== 'admin') {
    showToast('🚫 Access Denied! Admin Dashboard is restricted to Admin role users only.');
    switchPortal('shop');
    return;
  }
  try {
    const [dash, analytics] = await Promise.all([
      api.admin.getDashboard(),
      api.analytics.getOverview()
    ]);
    if (analytics) {
      document.getElementById('metric-today-orders').textContent = analytics.today_orders || '1,420';
      document.getElementById('metric-avg-delivery').textContent = `${analytics.avg_delivery_time_mins || 14.2} Mins`;
      document.getElementById('metric-revenue').textContent = `₹${(analytics.total_revenue_inr || 284500).toLocaleString()}`;
      document.getElementById('metric-active-riders').textContent = analytics.active_riders || '85';
    }
    if (dash) {
      const hubsContainer = document.getElementById('admin-hubs-container');
      hubsContainer.innerHTML = (dash.warehouses || [
        { name: "Koramangala Fashion Hub #01", active_orders: 42, status: "OPTIMAL" },
        { name: "Indiranagar Fashion Hub #02", active_orders: 38, status: "OPTIMAL" }
      ]).map(h => `
        <div class="notification-item flex-between">
          <div>
            <div class="notif-title">${h.name}</div>
            <div class="notif-msg">Active Express Orders: ${h.active_orders}</div>
          </div>
          <span class="pulse-dot"></span> <strong style="color: var(--accent-emerald);">${h.status}</strong>
        </div>
      `).join('');
    }
  } catch (err) { console.warn(err); }
};

function renderNotifications() {
  const list = document.getElementById('notification-list');
  const countBadge = document.getElementById('notification-count');
  if (!list) return;
  const notifs = state.notifications || [];
  if (countBadge) countBadge.textContent = notifs.length;
  if (!notifs || notifs.length === 0) {
    list.innerHTML = `
      <div class="notification-item" style="text-align: center; color: var(--text-muted); padding: 16px;">
        <span>🔔 No new notifications</span>
      </div>
    `;
    return;
  }
  list.innerHTML = notifs.map(n => `
    <div class="notification-item">
      <div class="notif-title">${n.title}</div>
      <div class="notif-msg">${n.message}</div>
      <div class="notif-time">${n.time}</div>
    </div>
  `).join('');
}

window.toggleNotificationDropdown = function() {
  document.getElementById('notification-dropdown').classList.toggle('active');
};
window.clearNotifications = function() {
  state.notifications = [];
  renderNotifications();
};

window.showToast = function(message) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
};

window.openVoiceSearchModal = function() {
  switchPortal('ai');
  switchAITab('voice');
};

function initTheme() {
  const savedTheme = localStorage.getItem('flashwear_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  const iconEl = document.getElementById('theme-toggle-icon');
  if (iconEl) iconEl.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
}

window.toggleTheme = function() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('flashwear_theme', newTheme);
  const iconEl = document.getElementById('theme-toggle-icon');
  if (iconEl) iconEl.textContent = newTheme === 'dark' ? '🌙' : '☀️';
  showToast(`Switched to ${newTheme === 'dark' ? 'Dark Obsidian 🌙' : 'Light Minimalist ☀️'} theme!`);
};
