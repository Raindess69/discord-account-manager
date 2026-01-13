# 🚀 Discord Account Manager & Token Injector

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A robust automation tool for managing multiple Discord accounts simultaneously without triggering anti-fraud systems. 

This project demonstrates advanced browser automation techniques, including **Webpack injection** and **Direct LocalStorage manipulation**, allowing for instant authentication via tokens (skipping the login screen).

## ⚡ Key Features

* **Token-Based Login:** Bypasses the standard login form by injecting authentication tokens directly into the browser's LocalStorage via Javascript execution.
* **Selenium 4 Integration:** Utilizes the latest Selenium WebDriver for stable and undetectable browser control.
* **Anti-Detection Module:** Includes a custom `Anti.crx` extension to mask WebDriver flags and emulate human fingerprints.
* **Webpack Injection:** Extracts and manipulates internal Discord Webpack modules to retrieve session data.
* **JSON Configuration:** Easy management of multiple accounts via `accs_example.json`.

## 🛠 Project Structure

* `discord_auth_manager.py` — The core automation logic and injection script.
* `Anti.crx` — Chrome extension for bypassing bot detection / fingerprint masking.
* `accs_example.json` — Configuration file for storing account tokens/credentials.
* `requirements.txt` — List of dependencies.

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Raindess69/discord-account-manager.git](https://github.com/Raindess69/discord-account-manager.git)
    cd discord-account-manager
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare your accounts:**
    Rename `accs_example.json` (or edit it directly) and add your Discord tokens.

## 🚀 Usage

Run the main script:

```bash
python discord_auth_manager.py
