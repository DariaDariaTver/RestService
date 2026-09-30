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
- order_statuses
- payment_methods
- refresh_tokens

### roles
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор роли |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Название роли (user, admin, manager, courier) |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### users
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор пользователя |
| role_id | INTEGER | NOT NULL, REFERENCES roles(id) | Роль пользователя |
| name | VARCHAR(100) | NOT NULL | Имя пользователя |
| email | VARCHAR(100) |UNIQUE, NOT NULL | Email пользователя |
| phone | VARCHAR(20)| UNIQUE, NOT NULL | Номер телефона пользователя |
| pw_hash | VARCHAR(255) | NOT NULL | Хеш пароля |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи | 
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### categories
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор категории |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Название категории |
| description | TEXT | | Описание категории |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### products
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор товара |
| category_id | INTEGER | NOT NULL, REFERENCES categories(id) | Категория товара |
| name | VARCHAR(100) | NOT NULL | Название блюда |
| description | TEXT | | Описание блюда |
| composition | TEXT | | Состав блюда |
| weight | NUMERIC(10, 2) | CHECK (weight > 0) | Вес блюда |
| price | NUMERIC(10, 2) | NOT NULL CHECK (price >= 0) | Цена блюда |
| image | VARCHAR(255) | | Путь к файлу изображения |
| is_available | BOOLEAN | DEFAULT TRUE | Флаг доступности товара в каталоге | 
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### carts
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор корзины |
| user_id | INTEGER | UNIQUE, NOT NULL, REFERENCES users(id) | Владелец корзины (у одного пользователя одна корзина)
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### cart_items
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор позиции в корзине |
| cart_id | INTEGER | NOT NULL, REFERENCES carts(id) | Корзина |
| product_id | INTEGER | NOT NULL, REFERENCES products(id) | Товар |
| quantity | INTEGER | NOT NULL | Количество товара |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |
| - | - | UNIQUE (cart_id, product_id) | Один товар в корзине встречается только раз |

### orders
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор заказа |
| user_id | INTEGER | NOT NULL, REFERENCES users(id) | Клиент, который оформил заказ |
| courier_id | INTEGER | REFERENCES users(id) | Курьер, назначенный на заказ |
| subtotal | NUMERIC(10, 2) | NOT NULL, CHECK (subtotal >= 0) | Сумма товаров |
| delivery_price | NUMERIC(10, 2) | NOT NULL, CHECK (delivery_price >= 0) | Стоимость доставки |
| total_price | NUMERIC(10, 2) | NOT NULL, CHECK (total_price >= 0) | Итоговая сумма (subtotal + delivery_price) |
| address_id | INTEGER | NOT NULL, REFERENCES addresses(id) | Адрес доставки |
| status_id | INTEGER | NOT NULL, REFERENCES order_statuses(id) | Статус заказа |
| payment_method_id | INTEGER | NOT NULL, REFERENCES payment_methods(id) | Способ оплаты |
| comment | TEXT | | Комментарии к заказу |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### order_items
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор позиции |
| order_id | INTEGER | NOT NULL, REFERENCES orders(id) | Заказ |
| product_id | INTEGER | NOT NULL, REFERENCES products(id) | Товар |
| quantity | INTEGER | NOT NULL, CHECK (quantity > 0) | Количество товара |
| price_at_moment | NUMERIC(10, 2) | NOT NULL, CHECK (price_at_moment >= 0) | Цена товара на момент оформления | 
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |
| - | - | UNIQUE (order_id, product_id) | Один товар в заказе встречается только раз |

### addresses
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор записи |
| user_id | INTEGER | NOT NULL, REFERENCES users(id) | Владелец адреса |
| city | VARCHAR(100) | NOT NULL | Город |
| street | VARCHAR(150) | NOT NULL | Улица |
| house | VARCHAR(20) | NOT NULL | Номер дома |
| apartment | VARCHAR(20) | | Номер квартиры |
| is_default | BOOLEAN | DEFAULT FALSE | Адрес доставки по умолчанию | 
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |

### order_statuses
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор статуса заказа |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Название статуса (new, confirmed, preparing, delivering, completed, cancelled)
| created_at | TIMESTAMP | DEFAULT NOW () | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW () | Дата последнего обновления записи |

### payment_methods 
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор способа оплаты |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Название способа оплаты (card, cash, online) | 
| created_at | TIMESTAMP | DEFAULT NOW () | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW () | Дата последнего обновления записи |

### refresh_tokens
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор токена |
| user_id | INTEGER | NOT NULL, REFERENCES users(id) | Владелец токена |
| token | VARCHAR(500) | UNIQUE, NOT NULL | Сам токен |
| expires_at | TIMESTAMP | NOT NULL | Дата истечения срока действия токена |
| revoked | BOOLEAN | DEFAULT FALSE | Флаг отзыва при логауте |
| created_at | TIMESTAMP | DEFAULT NOW() | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW() | Дата последнего обновления записи |


## Связи таблиц

### 1:N
- users -> addresses (У пользователя много адресов, адрес принадлежит одному пользователю)
- users -> orders (У одного пользователя много заказов, заказ на одного пользователя)
- users -> orders(courier) (У одного курьера много заказов, у заказа один курьер)
- categories -> products (В категории много товаров, для каждого одна категория)
- carts -> cart_items (В корзине много товаров, товар для одной корзины)
- orders -> order_items (В заказе несколько товаров, товар для конкретного заказа)
- addresses -> orders (На один адрес много заказов, заказ на один адрес)
- roles -> users (У роли много пользователей, у пользователя одна роль)
- users -> refresh_tokens (У пользователя много токенов, токен на одного пользователя)
- order_statuses -> orders (Один статус на много заказов, у заказа один статус)
- payment_methods -> orders (Один метод оплаты на много заказов, у заказа один метод оплаты)

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
CREATE INDEX idx_orders_payment_method_id ON orders(payment_method_id);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_orders_courier_id ON orders(courier_id)
```

## Методы

### Регистрация пользователя

#### POST /auth/register - Регистрация пользователя

**Запрос:**
```json
{
  "name": "Дарья",
  "email": "daria@mail.com",
  "phone": "+79123456789",
  "password": "password123"
}
```
**Ответ(201):**
```json
{
  "id": 22,
  "name": "Дарья",
  "email": "daria@mail.com",
  "phone": "+79123456789",
  "role_id": 1
}
```
#### POST /auth/login - Выдача токена

**Запрос:**
```json
{
  "email": "daria@mail.com",
  "password": "password123"
}
```
**Ответ(200):**
```json
{
  "access_token": "Ab3548fS...",
  "refresh_token": "jD4333g...",
  "token_type": "bearer"
  }
```
#### POST /auth/refresh - Обновление токена

**Запрос:**
```json
{
  "refresh_token": "jD4333g..."
}
```
**Ответ(200):**
```json
{
  "access_token": "Ab3548fS..."
}
```

### Пользователь

#### GET /users/me - Получить свой профиль

**Ответ(200):**
```json
{
  "id": 22,
  "name": "Дарья",
  "email": "daria@mail.com",
  "phone": "+7123456789",
  "role_id": 1
}
```

#### PUT /users/me - Обновить свой профиль

**Запрос:**
```json
{
  "name": "Дарья",
  "phone": "+7123456789"
}
```

**Ответ(200):**
```json
{
  "id": 22,
  "name": "Дарья",
  "email": "daria@mail.com",
  "phone": "+712345789",
  "role_id": 1
}
```

#### GET /users/me/addresses - Получить свои адреса

**Ответ(200):**
```json
[
{
  "id": 22,
  "city": "Тверь",
  "street": "Советская",
  "house": "12",
  "apartment": "34",
  "is_default": true
},
{
  "id": 23,
  "city": "Тверь",
  "street": "Фарафоновой",
  "house": "35",
  "apartment": null,
  "is_default": false
}
]
```
#### POST /users/me/addresses - Добавить адрес

**Запрос:**
```json
{
  "city": "Тверь",
  "street": "Фарафоновой",
  "house": "35",
  "apartment": "12",
  "is_default": false
}
```
**Ответ(200):**
```json
{
  "id": 24,
  "city": "Тверь",
  "street": "Фарафоновой",
  "house": "35",
  "apartment": "12",
  "is_default": false
}
```

#### PUT /users/me/addresses/{id} - Обновить текущий адрес 

**Запрос:**
```json
{
  "city": "Тверь",
  "street": "Фарафоновой",
  "house": "35",
  "apartment": "35",
  "is_default": true
}
```

**Ответ(200):**
```json
{
  "id": 23,
  "city": "Тверь",
  "street": "Фарафоновой",
  "house": "35",
  "apartment": "35",
  "is_default": true
}
```

#### DELETE /users/me/addresses/{id} - Удалить адрес

**Параметр пути:**
- id(int) - id адреса для удаления 

**Ответ(204)**

### Каталог

#### GET /categories - Показать все категории

**Параметры:**
- search(str) - поиск по названию 
- limit(int) - количество записей
- offset(int) - пропустить

**Пример запроса:**
GET /categories?search=суп&limit=20&offset=0

**Ответ(200):**
```json
{
  "items": [
    {"id": 1, "name": "Супы", "description": "Первые блюда"},
    {"id": 2, "name": "Горячее", "description": "Вторые блюда"}
  ],
  "total": 5,
  "limit": 20,
  "offset": 0,
  "pages": 1
}
```

#### GET /products - Показать все товары

**Параметры:**
- category_id(int) - фильтр по категории
- search(str) - поиск по названию
- min_price(float) - минимальная цена
- max_price(float) - максимальная цена 
- sort_by(str) - сортировка
- order(str) - направление
- limit(int) - количество записей
- offset(int) - пропустить 

**Пример запроса:**
GET /products?category_id=3&limit=20&offset=0

**Ответ(200):**
```json
{
  "items": [
    {
      "id": 11,
      "name": "Борщ",
      "price": 350.00,
      "is_available": true,
      "category_id": 3
    },
    {
      "id": 12,
      "name": "Пельмени домашние",
      "price": 300.00,
      "is_avaiable": true,
      "category_id": 4
    }
  ],
  "total": 45,
  "limit": 20,
  "offset": 0,
  "pages": 3
}
```

#### GET /products/{id} - Показать один товар

**Параметр пути:**
- id(int) - id товара

**Ответ(200):**
```json
{
  "id": 11,
  "name": "Борщ",
  "description": "С говядиной и сметаной",
  "composition": "Свекла, капуста, мясо, сметана",
  "price": 350.00,
  "weight": 300.00,
  "image": "/static/images/borsch.jpg",
  "is_available": true,
  "category_id": 3
}
```

### Корзина

#### GET /cart - Смотреть свою корзину

**Ответ(200):**
```json
{
  "id": 1,
  "items": [
    {
      "product_id": 11,
      "name": "Борщ",
      "quantity": 2,
      "price": 350.00
    },
    {
      "product_id": 27,
      "name": "Пельмени домашние",
      "quantity": 1,
      "price": 300.00
    }
  ],
  "total": 1000.00
}
```

#### POST /cart/items - Добавить товар в корзину

**Запрос:**
```json
{
  "product_id": 11,
  "quantity": 2
}
```

**Ответ(201):**
```json
{
  "id": 1,
  "items": [
    {
      "product_id": 11,
      "name": "Борщ",
      "quantity": 2,
      "price": 350.00
    }
  ],
  "total": 700.00
}
```

#### PUT /cart/items/{id} - Обновить количества товаров

**Параметр пути:**
- id(int) - id товара в корзине

**Запрос:**
```json
{
  "quantity": 3
}
```

**Ответ(200):**
```json
{
  "id": 1,
  "items": [
    {
      "product_id": 11,
      "name": "Борщ",
      "quantity": 3,
      "price": 350.00
    }
  ],
  "total": 1050.00
}
```

#### DELETE /cart/items/{id} - Удалить товар из корзины

**Параметр пути:**
- id(int) - id товара в корзине

**Ответ(204)**

### Заказы

#### POST /orders - Создать заказ из корзины

**Запрос:**
```json
{
  "address_id": 5,
  "payment_method_id": 1,
  "comment": "Домофон не работает, позвонить за 10 минут до приезда"
}
```

**Ответ(201):**
```json
{
  "id": 148,
  "user_id": 23,
  "status": "new",
  "subtotal": 1150.00,
  "delivery_price": 100.00,
  "total_price": 1250.00,
  "address": {
    "id": 5,
    "city": "Тверь",
    "street": "Советская",
    "house": "12",
    "apartment": "34"
  },
  "payment_method_id": 1,
  "comment": "Домофон не работает, позвонить за 10 минут до приезда",
  "items": [
    {
      "product_id": 11,
      "name": "Борщ",
      "quantity": 1,
      "price_at_moment": 350.00
    },
    {
      "product_id": 27,
      "name": "Пельмени домашние",
      "quantity": 2,
      "price_at_moment": 300.00
    },
    {
      "product_id": 42,
      "name": "Морс клюквенный",
      "quantity": 1,
      "price_at_moment": 200.00
    }
  ],
  "created_at": "2026-09-27T22:00:00Z"
}
```
#### GET /orders - Смотреть свои заказы

**Параметры:**
- status(str) - фильтр по статусу
- sort_by(str) - сортировка
- order(str) - направление
- limit(int) - количество записей
- offset(int) - пропуск

**Пример запроса:**
GET /orders?status=delivering&limit=20&offset=0

**Ответ(200):**
```json
{
  "items": [
    {
      "id": 148,
      "status": "delivering",
      "total_price": 1250.00,
      "created_at": "2026-09-24T22:00:00Z"
    }
  ],
  "total": 12,
  "limit": 20,
  "offset": 0,
  "pages": 1
}
```

#### GET /orders/{id} - Смотреть позиции заказа

**Параметр пути:**
-id(int) - id заказа

**Ответ(200):**
```json
{
  "id": 148,
  "user_id": 23,
  "status": "new",
  "subtotal": 1150.00,
  "delivery_price": 100.00,
  "total_price": 1250.00,
  "address": {
    "id": 5,
    "city": "Тверь",
    "street": "Советская",
    "house": "12",
    "apartment": "34"
    },
  "payment_method_id": 1,
  "comment": "Домофон не работает",
  "items": [
  {
  "product_id": 11,
  "name": "Борщ",
  "quantity": 1,
  "price_at_moment": 350.00
    }
  ],
  "created_at": "2026-09-27T22:00:00Z"
}
```

### Админка

#### POST /admin/categories - Создать категорию товаров

**Запрос:**
```json
{
  "name": "Супы",
  "description": "Первые блюда"
}
```

**Ответ(201):**
```json
{
  "id": 123,
  "name": "Супы",
  "description": "Первые блюда",
  "created_at": "2026-09-28T22:00:00Z"
}
```

#### PUT /admin/categories/{id} - Обновить категорию

**Параметр пути:**
- id(int) - id категории

**Запрос:**
```json 
{
  "name": "Горячие супы",
  "description": "Борщ, солянка, суп-пюре"
}
```

**Ответ(200):**
```json
{
  "id": 123,
  "name": "Горячие супы",
  "description": "Борщ, солянка, суп-пюре",
  "updated_at": "2026-09-28T22:00:00Z"
}
```

#### DELETE /admin/categories/{id} - Удалить категорию

**Параметр пути:**
- id(int) - id категории

**Ответ(204)**

#### POST /admin/products - Создать новый товар

**Запрос:**
```json
{
  "name": "Борщ",
  "description": "С говядиной и сметаной",
  "composition": "Свекла, капуста, мясо, сметана",
  "price": 350.00,
  "weight": 300.00,
  "category_id": 3,
  "image": "/static/images/borsch.jpg"
}
```

**Ответ(201):**
```json
{
  "id": 11,
  "name": "Борщ",
  "description": "С говядиной и сметаной",
  "composition": "Свекла, капуста, мясо, сметана",
  "price": 350.00,
  "weight": 300.00,
  "category_id": 3,
  "image": "/static/images/borsch.jpg",
  "is_available": true,
  "created_at": "2026-09-28T22:00:00Z"
}
```

#### PUT /admin/products/{id} - Обновить товар

**Параметр пути:**
- id(int) - id товара

**Запрос:**
```json
{
  "name": "Борщ Тверской",
  "description": "С говядиной, сметаной и пампушками",
  "composition": "Свекла, капуста, мясо, сметана, чеснок",
  "price": 400.00,
  "weight": 350.00,
  "category_id": 3,
  "image": "/static/images/borsch_new.jpg"
}
```

**Ответ(200):**
```json
{
  "id": 11,
  "name": "Борщ Тверской",
  "description": "С говядиной, сметаной и пампушками",
  "composition": "Свекла, капуста, мясо, сметана, чеснок",
  "price": 400.00,
  "weight": 350.00,
  "category_id": 3,
  "image": "/static/images/borsch_new.jpg",
  "is_available": true,
  "updated_at": "2026-09-28T22:00:00Z"
}
```

#### PATCH /admin/products/{id}/availability - Скрыть товар

**Параметр пути:**
- id(int) - id товара 

**Запрос:**
```json
{
  "is_available": false
}
```

**Ответ(200):**
```json
{
  "id": 11,
  "name": "Борщ Тверской",
  "is_available": false,
  "updated_at": "2026-09-28T22:00:00Z"
}
```

#### GET /admin/users - Смотреть всех пользователей

**Параметры:**
- search(str) - поиск пользователя по данным
- role_id(id) - фильтр по роли
- limit(int) - количество записей
- offset(int) - пропустить 

**Пример запроса:**
GET /admin/users?role_id=2&limit=20&offset=0

**Ответ(200):**
```json
{
  "items": [
    {
      "id": 23,
      "name": "Дарья",
      "email": "daria@mail.com",
      "phone": "+79123456789",
      "role_id": 1,
      "created_at": "2026-09-28T22:00:00Z"
    }
  ],
  "total": 154,
  "limit": 20,
  "offset": 0,
  "pages": 8
}
```

#### GET /admin/orders - Смотреть все заказы

**Параметры:**
- status(str) - фильтр по статусу
- user_id(int) -  фильтр по клиенту
- date_from(date) - заказы с даты ... (формат YYYY-MM-DD)
- date_to(date) - заказы по дату ... (формат YYYY-MM-DD)
- sort_by(str) - сортировка по дате, сумме заказов
- order(str) - направление
- limit(int) - количество записей
- offset(int) - пропустить

**Пример запроса:**
GET /admin/orders?status=new&limit=20&offset=0

**Ответ(200):**
```json
{
  "items": [
    {
      "id": 148,
      "user_id": 23,
      "courier_id": null,
      "status": "new",
      "total_price": 1250.00,
      "created_at": "2026-09-28T22:00:00Z"
    }
  ],
  "total": 3,
  "limit": 20,
  "offset": 0,
  "pages": 1
}
```

#### PUT /admin/orders/{id}/status - Изменить статус данного заказа

**Параметр пути:**
- id(int) - id заказа

**Запрос:**
```json
{
  "status_id": 2
}
```

**Ответ(200):**
```json
{
  "id": 148,
  "status": "confirmed",
  "updated_at": "2026-09-28T22:00:00Z"
}
```

#### PUT /admin/orders/{id}/courier - Назначить курьера

**Параметр пути:**
- id(int) - id заказа

**Запрос:**
```json
{
  "courier_id": 42
}
```

**Ответ(200):**
```json
{
  "id": 148,
  "courier_id": 42,
  "status": "delivering",
  "updated_at": "2026-09-28T22:00:00Z"
}
```

### Курьер

#### GET /courier/orders - Мои назначенные доставки

**Ответ:**
```json
{
  "items": [
    {
      "id": 148,
      "status": "delivering",
      "total_price": 1250.00,
      "address": {
        "city": "Тверь",
        "street": "Фарафоновой",
        "house": "35",
        "apartment": "33",
      },
      "created_at": "2026-09-24T22:00:00Z"
    }
  ]
}
```
#### PUT /courier/orders/{id}/status - Отметить заказ доставленным

**Параметр пути:**
- id(int) - id заказа

**Запрос:**
```json
{
  "status_id": 5
}
```

**Ответ(200)**
```json
{
  "id": 148,
  "status": "completed",
  "updated_at": "2026-09-28T22:00:00Z"
}
```

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