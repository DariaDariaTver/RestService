# Название

Бэкенд сервис для ресторана. Обеспечивает регистрацию пользователей, работу с каталогом блюд, работу с корзиной и управление заказами.

## Таблицы
- users 
- categories
- products
- carts
- cart_items
- orders
- order_items
- addresses

### users
- id 
- name 
- email
- phone
- pw_hash
- is_admin
- created_at

### categories
- id
- name
- description

### products
- id
- category_id
- name
- composition
- weight
- price
- image
- is_avialable

### carts
- id
- user_id
- created_at

### cart_items
- id
- cart_id
- product_id
- quantity

### orders
- id
- user_id
- total_price
- payment_method
- delivery_price
- comment
- address_id
- created_at
- status

### order_items
- id
- order_id
- product_id
- quantity
- price_at_moment

### addresses
- id
- user_id
- city
- street
- house
- apartment
- is_default




