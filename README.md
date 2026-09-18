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
- id (SERIAL, NOT NULL)
- name (VARCHAR(50), NOT NULL)
- email (VARCHAR(100), UNIQUE, NOT NULL)
- phone (VARCHAR(20), UNIQUE, NOT NULL)
- pw_hash (VARCHAR(255), NOT NULL)
- is_admin (BOOLEAN, DEFAULT FALSE, NOT NULL)
- created_at (TIMESTAMP, DEFAULT(NOW))

### categories
- id (SERIAL, NOT NULL)
- name (VARCHAR(50), NOT NULL)
- description (TEXT)

### products
- id (SERIAL, NOT NULL)
- category_id (INTEGER, NOT NULL)
- name (VARCHAR(100), NOT NULL)
- description (TEXT)
- composition (TEXT)
- weight (NUMERIC(10, 2))
- price (NUMERIC(10, 2), NOT NULL)
- image (VARCHAR(255))
- is_avialable (BOOLEAN, DEFAULT TRUE, NOT NULL)

### carts
- id (SERIAL, NOT NULL)
- user_id (INTEGER, UNIQUE, NOT NULL)
- created_at (TIMESTAMP, DEFAULT NOW(), NOT NULL)

### cart_items
- id (SERIAL, NOT NULL)
- cart_id (INTEGER, NOT NULL)
- product_id (INTEGER, NOT NULL)
- quantity (INTEGER, NOT NULL)

### orders
- id (SERIAL, NOT NULL)
- user_id (INTEGER, NOT NULL)
- total_price (NUMERIC(10, 2), NOT NULL)
- payment_method (VARCHAR(50), NOT NULL)
- delivery_price (NUMERIC(10, 2), NOT NULL)
- comment (TEXT)
- address_id (INTEGER, NOT NULL)
- created_at (TIMESTAMP, DEFAULT NOW(), NOT NULL)
- status (VARCHAR(30), DEFAULT 'new', NOT NULL)

### order_items
- id (SERIAL, NOT NULL)
- order_id (INTEGER, NOT NULL)
- product_id (INTEGER, NOT NULL)
- quantity (INTEGER, NOT NULL)
- price_at_moment (NUMERIC(10, 2), NOT NULL)

### addresses
- id (SERIAL, NOT NULL)
- user_id (INTEGER, NOT NULL)
- city (VARCHAR(30), NOT NULL)
- street (VARCHAR(30), NOT NULL)
- house (VARCHAR(10), NOT NULL)
- apartment (VARCHAR(10))
- is_default (BOOLEAN, DEFAULT FALSE, NOT NULL)

## Связи таблиц

### 1:N
- users -> addresses (У пользователя много адресов, адрес принадлежит одному пользователю)
- users -> orders (У одного пользователя много заказов, заказ на одного пользователя)
- categories -> products (В категории много товаров, для каждого одна категория)
- carts -> cart_items (В корзине много товаров, товар для одной корзины)
- orders -> order_items (В заказе несколько товаров, товар для конкретного заказа)
- addresses -> orders(На один адрес много заказов, заказ на один адрес)

### 1:1
- users -> carts (У пользователя одна корзина, корзина для одного  пользователя)

### N:M
- carts <-> products (В корзине много товаров, товар для многих корзин)
- orders <-> products (В заказе много товаров, товар для многих заказов)

## Методы

### Регистрация пользователя
- POST /auth/register - Регистрация пользователя
- POST /auth/login - Выдача токена
- POST /auth/refresh - Обновление токена

### Пользователь
- GET /users/me - Получить свой профиль
- PUT /users/me - Обновить свой профиль
- GET /users/me/addresses - Получить свои адреса
- POST /users/me/addresses - Добавить адрес
- PUT /users/me/addresses/{id} - Обновить текущий адрес 
- DELETE /users/me/addresses/{id} - Удалить адрес

### Каталог
- GET /categories - Показать все категории
- GET /products - Показать все товары
- GET /products/{id} - Показать один товар

### Корзина
- GET /cart - Смотреть свою корзину
- POST /cart/items - Добавить товар в корзину
- PUT /cart/items/{id} - Обновить количества товаров
- DELETE /cart/items/{id} - Удалить товар из корзины

### Заказы
- POST /orders - Создать заказ из корзины
- GET /orders - Смотреть свои заказы
- GET /orders/{id} - Смотреть позиции заказа

### Админка
- POST /admin/categories - Создать категорию товаров
- PUT /admin/categories/{id} - Обновить категорию
- DELETE /admin/categories/{id} - Удалить категорию
- POST /admin/products - Создать новый товар
- PUT /admin/products/{id} - Обновить товар
- DELETE /admin/products/{id} - Скрыть товар
- GET /admin/users - Смотреть всех пользователей
- GET /admin/orders - Смотреть все заказы
- PUT /admin/orders/{id}/status - Изменить статус данного заказа