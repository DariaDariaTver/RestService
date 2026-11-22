# Название

Бэкенд сервис для ресторана. Обеспечивает регистрацию пользователей, работу с каталогом блюд, работу с корзиной и управление заказами.

## Стек технологий
* **Язык:**  Python 3.12
* **Фреймворк:**  FastAPI
* **База данных:**  PostgreSQL
* **ORM:**  SQLAlchemy 2.0
* **Валидация данных:** Pydantic v2
* **Аутентификация:** JWT (Access + Refresh токены)
* **Безопасность:** bcrypt


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
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### users
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор пользователя |
| role_id | INTEGER | NOT NULL, REFERENCES roles(id) ON DELETE RESTRICT, INDEX | Роль пользователя |
| name | VARCHAR(100) | NOT NULL | Имя пользователя |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email пользователя |
| phone | VARCHAR(20)| UNIQUE, NOT NULL | Номер телефона пользователя |
| pw_hash | VARCHAR(255) | NOT NULL | Хеш пароля |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи | 
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### categories
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор категории |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Название категории |
| description | TEXT | | Описание категории |
| sort | INTEGER | DEFAULT 0 | Порядок отображения категории |
| is_visible | BOOLEAN | DEFAULT TRUE | Флаг видимости категории |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### products
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор товара |
| category_id | INTEGER | NOT NULL, REFERENCES categories(id), ON DELETE RESTRICT, INDEX | Категория товара |
| name | VARCHAR(100) | NOT NULL | Название блюда |
| description | TEXT | | Описание блюда |
| composition | TEXT | | Состав блюда |
| weight | NUMERIC(10, 2) | CHECK (weight > 0) | Вес блюда |
| price | NUMERIC(10, 2) | NOT NULL CHECK (price >= 0) | Цена блюда |
| image | VARCHAR(255) | | Путь к файлу изображения |
| is_available | BOOLEAN | DEFAULT TRUE | Флаг доступности товара в каталоге | 
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### carts
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор корзины |
| user_id | INTEGER | UNIQUE, NOT NULL, REFERENCES users(id), ON DELETE RESTRICT, INDEX | Владелец корзины (у одного пользователя одна корзина)
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### cart_items
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор позиции в корзине |
| cart_id | INTEGER | NOT NULL, REFERENCES carts(id), ON DELETE CASCADE| Корзина |
| product_id | INTEGER | NOT NULL, REFERENCES products(id), ON DELETE RESTRICT| Товар |
| quantity | INTEGER | NOT NULL | Количество товара |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |
| - | - | UNIQUE (cart_id, product_id) | Один товар в корзине встречается только раз |

### orders
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор заказа |
| user_id | INTEGER | NOT NULL, REFERENCES users(id), ON DELETE RESTRICT | Клиент, который оформил заказ |
| courier_id | INTEGER | REFERENCES users(id), ON DELETE SET NULL | Курьер, назначенный на заказ |
| subtotal | NUMERIC(10, 2) | NOT NULL, CHECK (subtotal >= 0) | Сумма товаров |
| delivery_price | NUMERIC(10, 2) | NOT NULL, CHECK (delivery_price >= 0) | Стоимость доставки |
| total_price | NUMERIC(10, 2) | NOT NULL, CHECK (total_price >= 0) | Итоговая сумма (subtotal + delivery_price) |
| address_id | INTEGER | NOT NULL, REFERENCES addresses(id), ON DELETE RESTRICT | Адрес доставки |
| status_id | INTEGER | NOT NULL, REFERENCES order_statuses(id), ON DELETE RESTRICT | Статус заказа |
| payment_method_id | INTEGER | NOT NULL, REFERENCES payment_methods(id), ON DELETE RESTRICT | Способ оплаты |
| comment | TEXT | | Комментарии к заказу |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### order_items
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор позиции |
| order_id | INTEGER | NOT NULL, REFERENCES orders(id), ON DELETE CASCADE, INDEX | Заказ |
| product_id | INTEGER | NOT NULL, REFERENCES products(id), ON DELETE RESTRICT, INDEX | Товар |
| quantity | INTEGER | NOT NULL, CHECK (quantity > 0) | Количество товара |
| price_at_moment | NUMERIC(10, 2) | NOT NULL, CHECK (price_at_moment >= 0) | Цена товара на момент оформления | 
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |
| - | - | UNIQUE (order_id, product_id) | Один товар в заказе встречается только раз |

### addresses
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор записи |
| user_id | INTEGER | NOT NULL, REFERENCES users(id), INDEX | Владелец адреса |
| city | VARCHAR(100) | NOT NULL | Город |
| street | VARCHAR(150) | NOT NULL | Улица |
| house | VARCHAR(20) | NOT NULL | Номер дома |
| apartment | VARCHAR(20) | | Номер квартиры |
| is_default | BOOLEAN | DEFAULT FALSE, NOT NULL | Адрес доставки по умолчанию | 
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата последнего обновления записи |

### order_statuses
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор статуса заказа |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Название статуса (new, confirmed, preparing, delivering, completed, cancelled)
| created_at | TIMESTAMP | DEFAULT NOW (), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW (), NOT NULL | Дата последнего обновления записи |

### payment_methods 
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор способа оплаты |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Название способа оплаты (card, cash, online) | 
| created_at | TIMESTAMP | DEFAULT NOW (), NOT NULL | Дата создания записи |
| updated_at | TIMESTAMP | DEFAULT NOW (), NOT NULL | Дата последнего обновления записи |

### refresh_tokens
| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AS IDENTITY | Уникальный идентификатор токена |
| user_id | INTEGER | NOT NULL, REFERENCES users(id), ON DELETE CASCADE, INDEX | Владелец токена |
| token | VARCHAR(500) | UNIQUE, NOT NULL | Сам токен |
| expires_at | TIMESTAMP | NOT NULL | Дата истечения срока действия токена |
| revoked | BOOLEAN | DEFAULT FALSE, NOT NULL | Флаг отзыва при логауте |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Дата создания записи |


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

**Ошибки:**
- 400 Bad Request - email, телефон уже существует или неверные данные
- 500 Internal Server Error - ошибка базы данных или сервера

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

**Ошибки:**
- 401 Unauthorized - невалидный или непереданный токен
- 500 Internal Server Error - ошибка базы данных или сервера

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

**Ошибки:**
- 401 Unauthorized - невалидный или отозванный refresh-токен
- 500 Internal Server Error - ошибка базы данных или сервера

### Пользователь

#### GET /auth/me - Получить свой профиль

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

#### POST /auth/logout - Выйти из системы

**Запрос:**
```json
{
  "refresh_token": "j28302ds..."
}
```

**Ответ(204)**

**Ошибки:**
- 204 No Content - успешный выход из системы

#### GET /addresses - Получить свои адреса

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

**Ошибки:**
- 500 Internal Server Error - ошибка базы данных или сервера

#### POST /addresses - Добавить адрес

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
**Ответ(201):**
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

**Ошибки:**
- 500 Internal Server Error - ошибка базы данных или сервера

#### PATCH /addresses/{id} - Обновить текущий адрес 

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

**Ошибки:**
- 404 Not Found - адрес не найден

#### DELETE /addresses/{id} - Удалить адрес

**Параметр пути:**
- id(int) - id адреса для удаления 

**Ответ(204)**

**Ошибки:**
- 404 Not Found - адрес не найден
- 204 No content - успешное удаление

### Каталог

#### GET /categories - Показать все категории

**Параметры:**
- search(str) - поиск по названию 
- limit(int) - количество записей
- page(int) - номер страницы

**Пример запроса:**
GET /categories?search=суп&page=1&limit=20

**Ответ(200):**
```json
{
  "items": [
    {"id": 1, "name": "Супы", "description": "Первые блюда"},
    {"id": 2, "name": "Горячее", "description": "Вторые блюда"}
  ],
  "total": 5,
  "page": 1,
  "pages": 1
}
```

#### GET /categories/{id} - Получить категорию по id

**Параметр пути:**
- id(int) - id категории

**Ответ(200):**
```json
{
  "id": 1,
  "name": "Супы",
  "description": "Первые блюда"
}
```

**Ошибки:**
- 404 Not Found - категория не найдена или скрыта

#### GET /products - Показать все товары

**Параметры:**
- category_id(int) - фильтр по категории
- search(str) - поиск по названию
- min_price(decimal) - минимальная цена
- max_price(decimal) - максимальная цена 
- sort_by(str) - сортировка
- order(str) - направление
- limit(int) - количество записей
- page(int) - номер страницы
- is_available - доступность товара

**Пример запроса:**
GET /products?category_id=3&page=1&limit=20

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
      "is_available": true,
      "category_id": 4
    }
  ],
  "total": 45,
  "limit": 20,
  "page": 1,
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

**Ошибки:**
- 404 Not Found - товар не найден

### Корзина

#### GET /cart - Смотреть свою корзину

**Ответ(200):**
```json
{
  "items": [
    {
      "id": 1,
      "quantity": 2,
      "product": {
        "id": 12,
        "name": "Борщ",
        "description": "Борщ со сметаной",
        "price": 350.00,
        "is_available": true
      },
      "total_price": "700.00"
    }
  ],
  "total_price": "700.00",
  "items_count": 2
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
  "quantity": 2,
  "product": {
    "id": 12,
    "name": "Борщ",
    "description": "Борщ со сметаной",
    "price": 350.00,
    "is_available": true
  },
  "total_price": "700.00"
}
```

**Ошибки:**
- 400 Bad Request - товара нет в наличии 
- 404 Not Found - товар не найден
- 409 Conflict - операция прервана

#### PATCH /cart/items/{id} - Обновить количество товара

**Параметр пути:**
- id(int) - id товара в корзине (CartItem ID)

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
  "quantity": 3,
  "product": {
    "id": 12,
    "name": "Борщ",
    "description": "Борщ со сметаной",
    "price": 350.00,
    "is_available": true
  },
  "total_price": "1050.00"
}
```

**Ошибки:**
- 404 Not Found - товар не найден
- 403 Forbidden - товар не принадлежит данной корзине

#### DELETE /cart/items/{id} - Удалить товар из корзины

**Параметр пути:**
- id(int) - id товара в корзине

**Ответ(204)**

**Ошибки:**
- 404 Not Found - товар не найден
- 403 Forbidden - товар не принадлежит данной корзине 
- 204 No Content - успешное удаление

#### DELETE /cart/clear - Очистить корзину

**Ответ(204)**

**Ошибки:**
- 204 No Content - успешное удаление

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

**Ошибки:**
- 404 Not Found - адрес, способ оплаты или статус заказа не найдены
- 400 Bad Request - корзина пуста или позиция корзины не в наличии 
- 500 Internal Server Error - ошибка базы данных или сервера

#### GET /orders - Смотреть свои заказы

**Параметры:**
- status(str) - фильтр по статусу
- sort_by(str) - сортировка
- order(str) - направление
- page(int) - номер страницы
- limit(int) - количество записей

**Пример запроса:**
GET /orders?status=delivering&page=1&limit=20

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
  "page": 1,
  "pages": 1
}
```

### Админка

#### GET /admin/categories - Список категорий в админке

**Параметры:**
- search(str) - поиск по названию
- page(int) - номер страницы
- limit(int) - количество записей

**Пример запроса:**
GET /admin/categories?search=soup&page=1&limit=20

**Ответ(200):**
```json
{
  "items": [ 
  {
  "id": 1,
  "name": "Супы",
  "description": "Первые блюда"
  }
],
"total": 5,
"limit": 20,
"page": 1,
"pages": 1
}
```

#### GET /admin/categories/{id} - Получить категорию по id

**Параметр пути:**
- id(int) - id категории

**Ответ(200):**
```json
{
  "id": 1,
  "name": "Супы",
  "description": "Первые блюда"
}
```

**Ошибки:**
- 404 Not Found - категория не найдена

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

**Ошибки:**
- 400 Bad Request - категория с таким именем уже существует 

#### PATCH /admin/categories/{id} - Обновить категорию

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

**Ошибки:**
- 404 Not Found - категория не найдена

#### DELETE /admin/categories/{id} - Удалить категорию

**Параметр пути:**
- id(int) - id категории

**Ответ(204)**

**Ошибки:**
- 404 Not Found - категория не найдена
- 204 No content - успешное удаление

#### GET /admin/products/{id} - Получить товар по id

**Параметр пути:**
- id(int) - id товара

**Ответ(200):**
```json
{
  "id": 22,
  "category_id": 3,
  "name": "Отбивная",
  "description": "Свиная отбивная с салатом",
  "composition": "Свинина, айсберг, соус",
  "weight": 400.00,
  "price": 650.00,
  "is_available": true,
  "image": "/static/images/otbivnaya.jpg"
}
```

**Ошибки:**
- 404 Not Found - товар не найден

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

**Ошибки:**
- 400 Bad Request - товар с таким именем уже существует или категория не найдена

#### PATCH /admin/products/{id} - Обновить товар

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

**Ошибки:**
- 404 Not Found - товар не найден
- 400 Bad Request - категория не найдена
- 500 Internal Server Error - ошибка базы данных или сервера

#### DELETE /admin/products/{id} - Удалить товар по id

**Параметр пути:**
- id(int) - id товара

**Ответ(204)**

**Ошибки:**
- 404 Not Found - товар не найден
- 204 No Content - успешное удаление

#### GET /admin/orders - Смотреть все заказы

**Параметры:**
- status(str) - фильтр по статусу
- user_id(int) -  фильтр по клиенту
- date_from(date) - заказы с даты ... (формат YYYY-MM-DD)
- date_to(date) - заказы по дату ... (формат YYYY-MM-DD)
- sort_by(str) - сортировка по дате, сумме заказов
- order(str) - направление
- limit(int) - количество записей
- page(int) - номер страницы

**Пример запроса:**
GET /admin/orders?status=new&page=1&limit=20

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
  "page": 1,
  "pages": 1
}
```

#### PATCH /admin/orders/{id}/status - Изменить статус данного заказа

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

**Ошибки:**
- 404 Not Found - заказ не найден
- 400 Bad Request - статус не найден или недопустимый переход статуса

#### PATCH /admin/orders/{id}/courier - Назначить курьера

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
  "user_id": 22,
  "courier_id": 42,
  "status": "new",
  "total_price": 1000.00,
  "updated_at": "2026-09-28T22:00:00Z"
}
```

**Ошибки:**
- 404 Not Found - заказ или пользователь не найден
- 400 Bad Request - пользователь не является курьером

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
        "apartment": "33"
      },
      "created_at": "2026-09-24T22:00:00Z"
    }
  ]
}
```
#### PATCH /courier/orders/{id}/status - Отметить заказ доставленным

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

**Ошибки:**
- 404 No Found - заказ не найден
- 403 Forbidden - заказ не принадлежит данному курьеру
- 400 Bad Request - нет статуса заказа или он невалидный

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