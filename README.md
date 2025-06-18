# Retejo

## Функции

 - **Валидация с помощью adaptix(и не только):** Используйте библиотеку **adaptix** для парсинга ответов. Вы можете с легкостью заменить **adaptix** на **pydantic**.
 - **Интуитивно понятный интерфейс:** Полностью типизированный клиент упрощает процесс разработки, устроняя множество ошибок ещё до запуска кода.
 - **Интеграции:** **Retejo** поддерживает интеграцию со такими клиентами как: **requests** и **aiohttp**.

## Установка

Вы можете установить **retejo** с помощью **pip**:

```bash
pip install retejo[requests]
pip install retejo[aiohttp]
```

или **uv**:

```bash
uv pip install retejo[requests]
uv pip install retejo[aiohttp]
```


## Написание кода.

Для начала нужно объявить модель, например, dataclass.

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

Потом нужно объявить метод.

В **retejo** каждый метод наследуется от базового класса Method. При наследовании в Method передается модель, которая описывает ответ метода.

Так же, нужно указать часть пусти к ендпоинту и тип метода.

```python
class GetPost(Method[Post]):
    __url__ = "posts/{id}"
    __method__ = "get"

    id: UrlVar[int]

class CreatePost(Method[PostId]):
    __url__ = "posts"
    __method__ = "post"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]
```

Теперь объявляем клиент. В super передаем базовую ссылку.

Так же переопределяем логику парсинга ответа.
За большей информацией по adaptix обратитесь к [его документации](https://adaptix.readthedocs.io/).

```python
class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__("https://jsonplaceholder.typicode.com/")

    @override
    def init_response_factory(self) -> Factory:
        return Retort(
            recipe=[
                # поля в ответе вида camelCase
                # будут конвертированы в lower_case.
                name_mapping(
                    name_style=NameStyle.CAMEL,
                ),
            ]
        )
```

Далее нужно привязать методы к клиенту. Для этого используется функция bind_method.

```python
class Client(RequestsClient):
    # ...
    get_post = bind_method(GetPost)
    create_post = bind_method(CreatePost)
```

Вы наверное подумаете, что из за этого не будет работать типизация. Наоборот, поведение будет как у метода, которая принимает аргументы для инициализации метода и возвращает ответ.

Например строка.

```python
get_post = bind_method(GetPost)
```

Эквивалентно следующему.

```
def get_post(self, id: int) -> Post:
    return self.send_method(
        GetPost(
            id=id,
        ),
    )
```

Типизация работает на все 100%.

И, конечно же, использование клиента.

```python
client = Client()
created_post = client.create_post(
    user_id=1,
    title="Title",
    body="Body"
)
got_post = client.get_post(created_post.id)
client.close()
```

Весь код.
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

class GetPost(Method[Post]):
    __url__ = "posts/{id}"
    __method__ = "get"

    id: UrlVar[int]

class CreatePost(Method[PostId]):
    __url__ = "posts"
    __method__ = "post"

    user_id: Body[int]
    title: Body[str]
    body: Body[str]


class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://jsonplaceholder.typicode.com/")

    @override
    def init_response_factory(self) -> Factory:
        return Retort(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )

    get_post = bind_method(GetPost)
    create_post = bind_method(CreatePost)


client = Client()
created_post = client.create_post(
    user_id=1,
    title="Title",
    body="Body"
)
got_post = client.get_post(created_post.id)
client.close()
```

## Асинхронность.

Для того, чтобы использовать асинхронный подход, нужно:

1. Установить retejo с aiohttp.

    ```bash
    pip install retejo[aiohttp]
    ```

2. Наследоваться от AiohttpClient.

3. Вызывать все методы клиента асинхронно.

    ```py
    class Client(AiohttpClient):
        def __init__(self) -> None:
            super().__init__(base_url="https://jsonplaceholder.typicode.com/")

    @override
    def init_response_factory(self) -> Factory:
        return Retort(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )

        get_post = bind_method(GetPost)
        create_post = bind_method(CreatePost)


    client = Client()
    created_post = await client.create_post(
        user_id=1,
        title="Title",
        body="Body"
    )
    got_post = await client.get_post(created_post.id)
    client.close()
    ```


## Маркеры

**Retejo** предоставляет несколько базовых маркеров для ваших методов:

- **Body** - параметр должен передано в **тело запроса**.

- **File** - параметр является **файлом**.

- **Header** - параметр должен передано в **заголовки запроса**.

- **QueryParam** - параметр должен передано в **параметры запроса**.

- **UrlVar** - параметр используется для **форматирования ссылки**.

- **Omittable** - этот флаг комбинируется с выше перечисленными. 

    Если значение параметра является объект **Omitted**, то это поле не попадет в запрос.

Пример использования.

```python
class AddModel(Method[Any]):
    __url__ = "user/{user_id}/models"
    __method__ = "post"

    user_id: UrlVar[int]
    model: Body[str]
    access_token: Header[str]
    number: Body[Omittable[str]] = Omitted()


class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__("")

    @override
    def init_markers_factories(self) -> MarkersFactorties:
        factories = super().init_markers_factories()
        factories[HeaderMarker] =  Retort(
            recipe=[
                dumper(
                    P[AddModel].access_token,
                    lambda x: f"Bearer {x}",
                ),
                name_mapping(
                    AddModel,
                    map={
                        "access_token": "Authorization",
                    },
                ),
            ],
        )
        return factories

    add_model = bind_method(AddModel)
```
