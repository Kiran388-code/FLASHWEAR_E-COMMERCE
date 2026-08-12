# User Roles
ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_RIDER = "rider"
ROLE_WAREHOUSE = "warehouse"

# Order Status
ORDER_PENDING = "pending"
ORDER_PAID = "paid"
ORDER_PROCESSING = "processing"
ORDER_SHIPPED = "shipped"
ORDER_DELIVERED = "delivered"
ORDER_CANCELLED = "cancelled"

# Pagination Defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Cache Keys
CACHE_USER_PREFIX = "user:"
CACHE_PRODUCT_PREFIX = "product:"

# Queue Names (RabbitMQ)
QUEUE_NOTIFICATIONS = "notifications_queue"
QUEUE_ANALYTICS = "analytics_queue"
QUEUE_ORDERS = "orders_queue"
