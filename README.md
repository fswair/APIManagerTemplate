# 🔐 API Request Manager

This Python template provides an easy-to-use, extensible, and secure way to authenticate and make HTTP requests to REST APIs using `aiohttp`, `pydantic`, and a flexible authentication model. It is well-suited for asynchronous applications interacting with APIs using either **Bearer Token** or **Basic Authentication**.

---

## 📦 Features

* ✅ Asynchronous requests using `aiohttp`
* ✅ Flexible authentication (Bearer Token or Basic Auth)
* ✅ Auto-generated `User-Agent`
* ✅ Smart URL joining with a custom `URL` type
* ✅ Structured configuration using `pydantic.BaseModel`

---

## 🚀 Installation

```bash
pip install aiohttp pydantic user-agent
```

---

## 📚 Classes Overview

### 🔗 `URL`

A subclass of `str` that allows safe path joining via the `/` operator.

```python
url = URL("https://api.example.com") / "users" / "42"
print(url)  # "https://api.example.com/users/42"
```

---

### 🔐 `AuthManager`

Manages base configuration for authentication and headers.

#### Parameters:

* `username`: Optional basic auth username
* `token`: Access token (used in bearer or basic)
* `base_url`: API base URL

#### Properties:

* `.user_agent`: Generates a dynamic User-Agent
* `.api_url`: Constructs full base API URL (e.g. `https://api.url/api/v1`)
* `.headers(bearer=True)`: Generates headers, optionally with bearer token

---

### 🌐 `RequestManager`

Inherits `AuthManager` and provides an asynchronous `.request()` method to perform API calls.

#### Method:

```python
async def request(endpoint: str, method: str = "GET", params: dict = None) -> dict
```

---

## 🧪 Example Use Case

```python
import asyncio
from auth import AuthManager, RequestManager

async def main():
    # Initialize authentication
    auth = AuthManager(
        username="myuser",                 # Optional: For Basic Auth
        token="ghp_xxxxxxx",              # Required
        base_url="https://api.github.com" # Example API
    )

    # Create request manager
    api = RequestManager(auth)

    # Make a GET request to "https://api.github.com/api/v1/user"
    response = await api.request("user")
    print(response)

asyncio.run(main())
```

---

## 🔄 Authentication Modes

| Type       | Configuration                      | Behavior                     |
| ---------- | ---------------------------------- | ---------------------------- |
| Bearer     | `username=None`, `bearer=True`     | Adds `Authorization: Bearer` |
| Basic Auth | `username != None`, `bearer=False` | Uses `aiohttp.BasicAuth`     |

---

## 📌 Notes

* This design makes it easy to wrap any REST API with minimal boilerplate.
* You can extend `RequestManager` to implement API-specific logic (e.g. `get_user`, `list_repos`, etc.)

---

## 🧱 Extending with Custom Methods

```python
class GitHubClient(RequestManager):
    async def get_user(self):
        return await self.request("user")

    async def list_repos(self):
        return await self.request("user/repos")
```

---

## 🛡️ License

**MIT License**
