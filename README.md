# 🚀 GorkProxy - Gork Proxy Cookie Rotation for GrokV3 Freedom, OpenAI API Compatible  
![GitHub Repo stars](https://img.shields.io/github/stars/CNFlyCat/GrokProxy?style=social)  ![GitHub forks](https://img.shields.io/github/forks/CNFlyCat/GrokProxy?style=social)  ![GitHub license](https://img.shields.io/github/license/CNFlyCat/GrokProxy)  

---  

## 📖 Introduction  
GorkProxy provides a **lightweight** proxy service that is **OpenAI API compatible**, supports **automatic cookie rotation**, and offers powerful configuration options. It also supports **Docker deployment** for easier usage! 🎉  

✨ **Key Features**:  
- 🏆 **Automatic Rotation** - Automatically switches cookies when request limits are reached.  
- 🔑 **Security** - Supports password authentication.  
- 🔄 **Easy Deployment** - Supports Docker and Docker Compose deployment.  

> ❗️ **Disclaimer**: This project is open-sourced under the MIT license. It is intended for learning and personal use only. Any legal issues arising from this project are the responsibility of the user. The author assumes no liability.

---

## 🔌 Fetching Gork Cookies  

1. Go to the [Gork official website](https://x.ai/) and register or log in to your account.  
2. Start a new chat session and press **F12** to open the browser Developer Console.  
3. Send any message to the AI to generate a request using your cookie.  
4. Navigate to the **Network** tab in the Developer Console.  
5. Look for a request named **"new"** or **"responses"** and click on it.  
6. Find the _Cookies_ section and look for an entry starting with **"sso="** (e.g., `sso=xdfdafAftda.sastwer... ;`).  
7. Copy the **entire value up to the semicolon (`;`)** and save it for later use in the configuration file.

---

## 🛠️ Installation & Deployment  

> ❗️ **Note**: Your deployment environment must be in a region where Gork services are officially available; otherwise, responses may not work properly!  

You can deploy with **Docker** or **Docker Compose**. Follow the steps below to set up the proxy.  

### ❇️ Clone from GitHub  

```sh
git clone https://github.com/CNFlyCat/GrokProxy.git
```
  
### 📝 Configure the Settings  

Open the `cookies.yaml` file and configure your cookies and authentication password:  

```sh
sudo nano cookies.yaml
```

```yaml
cookies:
  - "sso=AAAAAA-xxxxx"
  - "sso=fasdfas-xxxxx"
password: "your_password"
```

---

## 📦 Deploy Using Docker Compose (Recommended)  

### Modify the Docker Compose Configuration (Optional)  
Modify the `ports` settings to change the port mapping as needed:  

```yaml
services:
  app:
    image: grokproxy
    ports:
      - "8080:8000"
    volumes:
      - ./cookies.yaml:/app/cookies.yaml
```

### Build the Project  

```sh
docker-compose build
```

### Start the Project  

```sh
docker-compose up -d
```

---

## 🐳 Deploy Using Docker  

> **Note**: The following commands must be executed inside the project directory.  

### Build the Project  

```sh
docker build -t grokproxy .
```

### Run the Project  

```sh
docker run -d -p 8080:8000 -v ./cookies.yaml:/app/cookies.yaml grokproxy
```

---

## 📖 Using the Proxy  

🎉 Now, you can use OpenWebUI or any OpenAI API-compatible AI frontend.  

- **Local:** `http://127.0.0.1:8080/v1`  
- **Remote:** `http://(your_domain_or_IP):8080/v1`  

Enter your configured password or API key when prompted. Then, send a test message – If everything is set up correctly, you will receive a response from Gork! 🚀  

---

## 🔗 Open-Source Repository  

🌟 **Star & Fork are Welcome!**  

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/CNFlyCat/GrokProxy)  
[![Issues](https://img.shields.io/github/issues/CNFlyCat/GrokProxy?color=red&logo=github)](https://github.com/CNFlyCat/GrokProxy/issues)  
[![Pull Requests](https://img.shields.io/github/issues-pr/CNFlyCat/GrokProxy?color=green&logo=github)](https://github.com/CNFlyCat/GrokProxy/pulls)  

---

RocketCat  
2025/2/26
