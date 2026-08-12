/**
 * FLASHWEAR API Client Module
 */

const API_BASE_URL = '/api';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('flashwear_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = { ...options, headers };

  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, config);
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: res.statusText }));
      const msg = (errorData.error && errorData.error.message) || errorData.detail || errorData.message || `HTTP Error ${res.status}`;
      throw new Error(msg);
    }
    return await res.json();
  } catch (err) {
    console.warn(`[API Call Warning] ${endpoint}:`, err.message);
    throw err;
  }
}

export const api = {
  auth: {
    login: (username, password) => {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      return fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      }).then(res => res.json());
    },
    loginJson: (email, password) => request('/auth/login-json', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),
    register: (userData) => request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    }),
    logout: () => request('/auth/logout', { method: 'POST' }),
    sendOTP: (contact) => request('/auth/otp/send', {
      method: 'POST',
      body: JSON.stringify({ contact })
    }),
    verifyOTP: (contact, code) => request('/auth/otp/verify', {
      method: 'POST',
      body: JSON.stringify({ contact, code })
    }),
    verifyLink: (token, email) => request(`/auth/otp/verify-link?token=${encodeURIComponent(token)}&email=${encodeURIComponent(email)}`),
    validateEmail: (contact) => request('/auth/otp/validate-email', {
      method: 'POST',
      body: JSON.stringify({ contact })
    })
  },
  users: { getMe: () => request('/users/me') },
  products: {
    list: (category = '', search = '') => {
      const params = new URLSearchParams();
      if (category && category !== 'all') params.append('category', category);
      if (search) params.append('search', search);
      const query = params.toString() ? `?${params.toString()}` : '';
      return request(`/products/${query}`);
    },
    getById: (id) => request(`/products/${id}`)
  },
  category: { list: () => request('/category/') },
  brand: { list: () => request('/brand/') },
  cart: {
    get: () => request('/cart/'),
    addItem: (item) => request('/cart/items', {
      method: 'POST',
      body: JSON.stringify(item)
    }),
    removeItem: (itemId) => request(`/cart/items/${itemId}`, { method: 'DELETE' }),
    clear: () => request('/cart/clear', { method: 'DELETE' })
  },
  checkout: {
    process: (orderData) => request('/checkout/process', {
      method: 'POST',
      body: JSON.stringify(orderData)
    })
  },
  orders: {
    list: (userId = 1) => request(`/orders/?user_id=${userId}`),
    getByNumber: (orderNumber) => request(`/orders/${orderNumber}`),
    updateStep: (orderNumber, stepNumber) => request(`/orders/${orderNumber}/step`, {
      method: 'PATCH',
      body: JSON.stringify({ step_number: stepNumber })
    })
  },
  rider: {
    getProfile: (riderId = 101) => request(`/rider/profile?rider_id=${riderId}`),
    getAssignedOrders: (riderId = 101) => request(`/rider/assigned-orders?rider_id=${riderId}`),
    acceptOrder: (orderNumber) => request(`/rider/accept-order/${orderNumber}`, { method: 'POST' }),
    updateLocation: (riderId, lat, lng) => request('/rider/location', {
      method: 'POST',
      body: JSON.stringify({ rider_id: riderId, current_lat: lat, current_lng: lng })
    }),
    verifyOTP: (orderId, otp) => request('/rider/verify-otp', {
      method: 'POST',
      body: JSON.stringify({ order_id: orderId, otp })
    })
  },
  warehouse: {
    getPickList: (orderNumber) => request(`/warehouse/pick-list/${orderNumber}`),
    scanBarcode: (orderId, barcode) => request('/warehouse/scan-barcode', {
      method: 'POST',
      body: JSON.stringify({ order_id: orderId, barcode })
    }),
    dispatch: (orderNumber) => request(`/warehouse/dispatch/${orderNumber}`, { method: 'POST' })
  },
  admin: { getDashboard: () => request('/admin/dashboard') },
  analytics: { getOverview: () => request('/analytics/overview') },
  ai: {
    virtualTryOn: (productId, userImageBase64) => request('/ai/virtual-try-on', {
      method: 'POST',
      body: JSON.stringify({ product_id: parseInt(productId), user_image_base64: userImageBase64 })
    }),
    sizeRecommendation: (heightCm, weightKg, fitPreference) => request('/ai/size-recommendation', {
      method: 'POST',
      body: JSON.stringify({ height_cm: parseInt(heightCm), weight_kg: parseInt(weightKg), fit_preference: fitPreference })
    }),
    voiceSearch: (transcript) => request('/ai/voice-search', {
      method: 'POST',
      body: JSON.stringify({ transcript })
    }),
    chatbot: (message) => request('/ai/chatbot', {
      method: 'POST',
      body: JSON.stringify({ message })
    })
  },
  reviews: {
    get: (productId) => request(`/review/${productId}`),
    add: (reviewData) => request('/review/', {
      method: 'POST',
      body: JSON.stringify(reviewData)
    })
  },
  notifications: { get: () => request('/notification/') }
};
