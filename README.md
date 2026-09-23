# Название

Бэкенд сервис для ресторана. Обеспечивает регистрацию пользователей, работу с каталогом блюд, работу с корзиной и управление заказами.

## Таблицы
- roles
- users 
- categories
- products
- carts
- cart_items
- orders
- order_items
- addresses

### roles
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- name VARCHAR(100) UNIQUE NOT NULL
- created_at TIMESTAMP DEFAULT NOW()
- updated_at TIMESTAMP DEFAULT NOW()

### users
- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
- role_id INTEGER NOT NULL REFERENCES roles(id)
- name VARCHAR(100) NOT NULL
- email VARCHAR(100) UNIQUE NOT NULL
- phone VARCHAR(20) UNIQUE NOT NULL
- pw_hash VARCHAR(255) NOT NULL 
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
- image VARCHAR(255) - ссылка на файл в папке
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
- total_price NUMERIC(10, 2) NOT NULL CHECK (total_price >= 0) - итоговая сумма (subtotal + delivery_price)
- address_id INTEGER NOT NULL REFERENCES addresses(id)
- status_id INTEGER NOT NULL REFERENCES order_statuses(id)
- payment_method_id INTEGER NOT NULL REFERENCES payment_methods(id)
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
- addresses -> orders (На один адрес много заказов, заказ на один адрес)
- roles -> users (У роли много пользователей, у пользователя одна роль)
- order_statuses -> orders (Один статус на много заказов, у заказа один статус)
- payment_methods -> orders (Один метод оплаты на много заказов, у заказа один метод)

### 1:1
- users -> carts (У пользователя одна корзина, корзина для одного  пользователя)

### N:M
- carts <-> products (В корзине много товаров, товар для многих корзин. Реализуется через cart_items)
- orders <-> products (В заказе много товаров, товар для многих заказов. Реализуется через order_items)

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
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_orders_status_id ON orders(status_id);
CREATE INDEX idx_orders_payment_method_id ON orders(payment_method_id)
```

## Методы

### Регистрация пользователя
- POST /auth/register - Регистрация пользователя
  - Принимает: name, email, phone, password
  - Возвращает: данные нового пользователя
- POST /auth/login - Выдача токена
  - Принимает: email, password
  - Возвращает: access_token, refresh_token
- POST /auth/refresh - Обновление токена
  - Принимает: refresh_token
  - Возвращает: новый access_token

### Пользователь
- GET /users/me - Получить свой профиль
- PUT /users/me - Обновить свой профиль
- GET /users/me/addresses - Получить свои адреса
- POST /users/me/addresses - Добавить адрес
- PUT /users/me/addresses/{id} - Обновить текущий адрес 
- DELETE /users/me/addresses/{id} - Удалить адрес

### Каталог
- GET /categories - Показать все категории
  - Параметры: search, limit, offset

- GET /products - Показать все товары
  - Параметры: category_id, search, min_price, max_price, sort_by, order, limit, offset
  - Пример: GET /products?category_id=3&limit=20&offset=0
- GET /products/{id} - Показать один товар

### Корзина
- GET /cart - Смотреть свою корзину
  - Возвращает: корзину с товарами
- POST /cart/items - Добавить товар в корзину
  - Принимает: product_id, quantity
  - Возвращает: обновленную корзину
- PUT /cart/items/{id} - Обновить количества товаров
  - Принимает: quantity
  - Возвращает: новое количество товаров 
- DELETE /cart/items/{id} - Удалить товар из корзины
  - Возвращает: обновленную корзину 

### Заказы
- POST /orders - Создать заказ из корзины
  - Принимает: address_id, payment_method, comment
  - Возвращает: созданный заказ 
- GET /orders - Смотреть свои заказы
  - Параметры: status, sort_by, order, limit, offset
  - Возвращает: список заказов
- GET /orders/{id} - Смотреть позиции заказа
  - Возвращает: заказ с его характеристиками 

### Админка
- POST /admin/categories - Создать категорию товаров
  - Принимает: name, description
  - Возвращает: созданную категорию
- PUT /admin/categories/{id} - Обновить категорию
  - Принимает: name, description
  - Возвращает: обновленную категорию 
- DELETE /admin/categories/{id} - Удалить категорию
  - Возвращает: информацию об удалении 
- POST /admin/products - Создать новый товар
  - Принимает: name, description, price, weight, image, category_id
  - Возвращает: новый товар
- PUT /admin/products/{id} - Обновить товар
  - Принимает: name, description, price, weight, image, category_id
  - Возвращает: обновленный товар
- DELETE /admin/products/{id} - Скрыть товар
  - Возвращает: сообщение об удалении
- GET /admin/users - Смотреть всех пользователей
  - Параметры: search, role_id, limit, offset
- GET /admin/orders - Смотреть все заказы
  - Параметры: status, user_id, date_from, date_to, sort_by, order, limit, offset
- PUT /admin/orders/{id}/status - Изменить статус данного заказа
  - Принимает: status_id
  - Возвращает: обновленный статус 

## Справочник

**roles** - роль пользователя:
- user
- admin
- manager
- courier

**order_statuses** - статус заказа:
- new
- confirmed
- preparing
- delivering
- completed
- cancelled

**payment_methods** - способ оплаты:
- online
- cash
- card