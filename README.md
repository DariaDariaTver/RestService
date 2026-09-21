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
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- name VARCHAR(100) NOT NULL
- email VARCHAR(100) UNIQUE NOT NULL
- phone VARCHAR(20) UNIQUE NOT NULL
- pw_hash VARCHAR(255) NOT NULL
- is_admin BOOLEAN DEFAULT FALSE 
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### categories
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- name VARCHAR(100) UNIQUE NOT NULL
- description TEXT
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### products
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- category_id INTEGER NOT NULL REFERENCES categories(id)
- name VARCHAR(100) NOT NULL
- description TEXT
- composition TEXT
- weight NUMERIC(10, 2) CHECK (weight > 0)
- price NUMERIC(10, 2) NOT NULL CHECK (price >= 0) 
- image VARCHAR(255)
- is_available BOOLEAN DEFAULT TRUE 
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### carts
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- user_id INTEGER UNIQUE NOT NULL REFERENCES users(id)
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### cart_items
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- cart_id INTEGER NOT NULL REFERENCES carts(id)
- product_id INTEGER NOT NULL REFERENCES products(id)
- quantity INTEGER NOT NULL
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()
- UNIQUE (cart_id, product_id)

### orders
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- user_id INTEGER NOT NULL REFERENCES users(id)
- subtotal NUMERIC(10, 2) NOT NULL CHECK (subtotal >= 0)
- delivery_price NUMERIC(10, 2) NOT NULL CHECK (delivery_price >= 0)
- total_price NUMERIC(10, 2) NOT NULL CHECK (total_price >= 0)
- address_id INTEGER NOT NULL REFERENCES addresses(id)
- status VARCHAR(30) DEFAULT 'new' NOT NULL
- payment_method VARCHAR(50) NOT NULL
- comment TEXT
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### order_items
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- order_id INTEGER NOT NULL REFERENCES orders(id)
- product_id INTEGER NOT NULL REFERENCES products(id)
- quantity INTEGER NOT NULL CHECK (quantity > 0)
- price_at_moment NUMERIC(10, 2) NOT NULL CHECK (price_at_moment >= 0) 
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()
- UNIQUE (order_id, product_id)

### addresses
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- user_id INTEGER NOT NULL REFERENCES users(id)
- city VARCHAR(30) NOT NULL
- street VARCHAR(30) NOT NULL
- house VARCHAR(10) NOT NULL
- apartment VARCHAR(10)
- is_default BOOLEAN DEFAULT FALSE 
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

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

## Индексы

``` sql 
CREATE INDEX idx_addresses_user_id ON addresses(user_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_carts_user_id ON carts(user_id);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_address_id ON orders(address_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id)
```

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