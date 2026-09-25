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
| id | INTEGER | PRIMARY KEY, GENERATED ALWAYS AD IDENTITY | Уникальный идентификатор статуса заказа |
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