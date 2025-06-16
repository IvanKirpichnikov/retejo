# Retejo

A modern and simple way to create clients for **REST** like APIs

## Advantages
1. Fully typable library.
2. Supports async and sync.
3. Simple and intuitive user API.


## Quickstart

**Step 1.** Install library.

```bash
pip install retejo requests
```

**Step 2.** Declare model.

```python
@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int
```

**Step 3.** Declare methods.

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


**Step 4.** Declare client.

```python
class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://jsonplaceholder.typicode.com/")

    @override
    def _init_response_factory(self) -> Retort:
        retort = super()._init_response_factory()
        return retort.extend(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )
```

**Step 5.** Bind methods to clients.

```python
class Client(RequestsClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://jsonplaceholder.typicode.com/")

    @override
    def _init_response_factory(self) -> Retort:
        retort = super()._init_response_factory()
        return retort.extend(
            recipe=[
                name_mapping(name_style=NameStyle.CAMEL),
            ]
        )

    get_post = bind_method(GetPost)
    create_post = bind_method(CreatePost)
```

**Step 6.** Use client.

```python
client = Client()
created_post = client.create_post(
    user_id=1,
    title="Title",
    body="Body"
)
got_post = client.get_post(created_post.id)

```

**Step 7.** Close client.

```python
client.close()
```

**Full code.**
```python
@dataclass
class Post:
    id: int
    title: str
    body: str
    user_id: int


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
    def _init_response_factory(self) -> Retort:
        retort = super()._init_response_factory()
        return retort.extend(
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

## Asyncio

To use async client insted of sync:

1. Install aiohttp (instead of requests)
2. Change RequestsClient to AiohttpClient
3. Add the await keyword before the method call

```py
class Client(AiohttpClient):
    def __init__(self) -> None:
        super().__init__(base_url="https://jsonplaceholder.typicode.com/")

    @override
    def _init_response_factory(self) -> Retort:
        retort = super()._init_response_factory()
        return retort.extend(
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


