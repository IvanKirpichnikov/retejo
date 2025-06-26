# Retejo

[![PyPI version](https://badge.fury.io/py/retejo.svg)](https://pypi.python.org/pypi/retejo)
[![Supported versions](https://img.shields.io/pypi/pyversions/retejo.svg)](https://pypi.python.org/pypi/retejo)
[![License](https://img.shields.io/github/license/IvanKirpichnikov/retejo)](https://github.com/IvanKirpichnikov/retejo/blob/master/LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/IvanKirpichnikov/retejo/setup.yml)](https://github.com/IvanKirpichnikov/retejo/actions)

---

**Retejo (ретейо)** — современная библиотека для декларативного описания web-клиентов с поддержкой валидации и полной типизацией

---

## Возможности

- **Валидация данных** через `adaptix` или `pydantic`.
- **Полная типизация** для раннего обнаружения ошибок.
- **Поддержка HTTP-клиентов**: `requests`, `aiohttp`, `httpx`.
- **Декларативное описание** методов.

---

## Установка

=== "adaptix"
    ```bash
    pip install retejo[requests, adaptix]
    pip install retejo[aiohttp, adaptix]
    pip install retejo[httpx, adaptix]
    ```

=== "pydantic"
    ```bash
    pip install retejo[requests, pydantic]
    pip install retejo[aiohttp, pydantic]
    pip install retejo[httpx, pydantic]
    ```

---

## Концепции

### 1. Декларативное описание методов. 

Каждый метод описывается как независимый класс, наследуюясь от базового класса Method и передавая тип ответ в Generic параметр Method

```python
class GetUser(Method[User]):
    __url__ = "users/{id}"
    __method__ = "GET"

    id: UrlVar[int]
    details: QueryParam[bool]
    access_token: Header[str]
```

### 2. Независимость от web клиента.

Любой метод можно **переиспользовать** с любым клиентом, ведь метод не привязан к ним

=== "requests"
    ```py
    class RequestsClient(RequestsAdaptixClient):
        def __init__(self) -> None:
            super().__init__("https://web.server.com/api")

        get_user = bind_method(GetUser)
    ```

=== "aiohttp"
    ```py
    class AiohttpClient(AiohttpAdaptixClient):
        def __init__(self) -> None:
            super().__init__("https://web.server.com/api")

        get_user = bind_method(GetUser)
    ```

=== "httpx (sync)"
    ```py
    class HttpxClient(HttpxAdaptixSyncClient):
        def __init__(self) -> None:
            super().__init__("https://web.server.com/api")

        get_user = bind_method(GetUser)
    ```

=== "httpx (async)"
    ```py
    class HttpxClient(HttpxAdaptixAsyncClient):
        def __init__(self) -> None:
            super().__init__("https://web.server.com/api")

        get_user = bind_method(GetUser)
    ```


---

## Базовое использование

### 1. Описание моделей

```python
@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


@dataclass
class PostId:
    id: int
```

---

### 2. Описание API-методов

```python
class GetPost(Method[Post]):
    __url__ = "posts/{id}"
    __method__ = "GET"

    id: UrlVar[int]  # Параметр URL


class CreatePost(Method[PostId]):
    __url__ = "posts"
    __method__ = "POST"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]
```

---

### 3. Создание клиента и переопределене логики парсинга ответа

=== "requests"
    ```python
    class JSONPlaceholderClient(RequestsAdaptixClient):
        def __init__(self):
            super().__init__("https://jsonplaceholder.typicode.com/")

        def init_response_factory(self) -> Retort:
            return super().init_response_factory().extend(
                recipe=[
                    # camelCase -> lower_case
                    name_mapping(name_style=NameStyle.CAMEL)
                ]
            )

        get_post = bind_method(GetPost)
        create_post = bind_method(CreatePost)
    ```

=== "aiohttp"
    ```python
    class JSONPlaceholderClient(AiohttpAdaptixClient):
        def __init__(self):
            super().__init__("https://jsonplaceholder.typicode.com/")

        def init_response_factory(self) -> Retort:
            return super().init_response_factory().extend(
                recipe=[
                    # camelCase -> lower_case
                    name_mapping(name_style=NameStyle.CAMEL)
                ]
            )

        get_post = bind_method(GetPost)
        create_post = bind_method(CreatePost)
    ```

=== "httpx (sync)"
    ```python
    class JSONPlaceholderClient(HttpxAdaptixSyncClient):
        def __init__(self):
            super().__init__("https://jsonplaceholder.typicode.com/")

        def init_response_factory(self) -> Retort:
            return super().init_response_factory().extend(
                recipe=[
                    # camelCase -> lower_case
                    name_mapping(name_style=NameStyle.CAMEL)
                ]
            )

        get_post = bind_method(GetPost)
        create_post = bind_method(CreatePost)
    ```

=== "httpx (async)"
    ```python
    class JSONPlaceholderClient(HttpxAdaptixAsyncClient):
        def __init__(self):
            super().__init__("https://jsonplaceholder.typicode.com/")

        def init_response_factory(self) -> Retort:
            return super().init_response_factory().extend(
                recipe=[
                    # camelCase -> lower_case
                    name_mapping(name_style=NameStyle.CAMEL)
                ]
            )

        get_post = bind_method(GetPost)
        create_post = bind_method(CreatePost)
    ```

!!! tip
    Возможно, вы подумаете, что использование `bind_method` ломает типизиацию, но это не так.

    ```py
    get_post = bind_method(GetPost)
    ```

    Полностью экваивалентно

    ```py
    (async) def get_post(self, *, id: UrlVar[int]) -> Post:
        return await self.send_method(GetPost(id=id))
    ```

### 4. Использование клиента

=== "requests"
    ```python
    with JSONPlaceholderClient() as client:
        # Создание поста
        new_post = client.create_post(
            user_id=1,
            title="Hello Retejo",
            body="This is a test post"
        )

        # Получение поста
        post = client.get_post(id=new_post.id)
    ```

=== "aiohttp"
    ```python
    async with JSONPlaceholderClient() as client:
        # Создание поста
        new_post = await client.create_post(
            user_id=1,
            title="Hello Retejo",
            body="This is a test post"
        )

        # Получение поста
        post = await client.get_post(id=new_post.id)
    ```

=== "httpx (sync)"
    ```python
    with JSONPlaceholderClient() as client:
        # Создание поста
        new_post = client.create_post(
            user_id=1,
            title="Hello Retejo",
            body="This is a test post"
        )

        # Получение поста
        post = client.get_post(id=new_post.id)
    ```

=== "httpx (async)"
    ```python
    async with JSONPlaceholderClient() as client:
        # Создание поста
        new_post = await client.create_post(
            user_id=1,
            title="Hello Retejo",
            body="This is a test post"
        )

        # Получение поста
        post = await client.get_post(id=new_post.id)
    ```

---

## Маркеры параметров

С помощью маркеров помечают куда нужно сопоставить данные параметра при отправке запроса

Retejo предоставляет 6 видов маркеров

| Маркер       | Назначение                                             | Пример                                  |
|--------------|--------------------------------------------------------|-----------------------------------------|
| `Body`       | Тело запроса (application/json)                        | `title: Body[str]`                      |
| `File`       | Файл (multipart/form-data)                             | `avatar: File`                          |
| `Header`     | Заголовок запроса                                      | `auth: Header[str]`                     |
| `QueryParam` | Параметр URL (?key=value)                              | `page: QueryParam[int]`                 |
| `UrlVar`     | Переменная пути URL (/end/{param})                     | `id: UrlVar[int]`                       |
| `Omittable`  | Параметр опускается, если значение является Omitted()  | `opt: Body[Omittable[str]] = Omitted()` |

---

### Кастомная обработка маркеров

Обработку каждого маркера можно с легкостью переопределить.


Давайте добавим пару рецептов для фабрики HeaderMarker.
Опишем, что при отправке запроса:

1. Должен добавиться тип токена `Bearer`.
2. Должно поменяться имя хедера с access_token на Authorization

```python
class AddModel(Method[Any]):
    __url__ = "user/{user_id}/models"
    __method__ = "POST"

    user_id: UrlVar[int]
    model_name: Body[str]
    access_token: Header[str]
    description: Body[Omittable[str]] = Omitted()


class CustomClient(RequestsAdaptixClient):
    def init_markers_factories(self) -> MarkersFactories[Retort]:
        factories = super().init_markers_factories()
        factories[HeaderMarker].extend(
            recipe=[
                dumper(
                    lambda x: f"Bearer {x}",  # Преобразование значения
                    P[AddModel].access_token
                ),
                name_mapping(
                    AddModel,
                    map={"access_token": "Authorization"}  # Имя заголовка
                )
            ]
        )
        return factories
```

---

## Интеграции

---

### Поддерживаемые HTTP-клиенты

- `requests` - синхронный
- `aiohttp` - асинхронный
- `httpx` - синхронный/асинхронный

---

### Поддерживаемые валидаторы

- `adaptix` (рекомендуется)
- `pydantic (v2)`

---

## Преимущества использования

1. **Декларативный подход** - чёткое разделение описания методов и клиента.
2. **Автоматическая валидация** - данных запроса и ответа.
3. **Полная типизация** - позволяет обнаружить ошибки до запуска кода.
4. **Гибкая конфигурация** - кастомизация всех аспектов запроса.
5. **Единый стиль** - для синхронного и асинхронного кода.

---

## Сообщество и поддержка

- [GitHub репозиторий](https://github.com/IvanKirpichnikov/retejo)
- [Отслеживание проблем](https://github.com/IvanKirpichnikov/retejo/issues)
- [Примеры использования](https://github.com/IvanKirpichnikov/retejo/tree/main/examples)
