# 🧪 Web Automation Framework (Selenium, Python, Pytest & Allure)

A modular, scalable, and ready-to-use **Test Automation Framework** built with **Selenium WebDriver**, **Python**, **Pytest**, and **Allure Reporting**. Designed with a robust architecture following the **Page Object Model (POM)** and best practices in automation for ease of use, reusability, and maintainability.

---

## 🚀 Tech Stack

- ✅ **Selenium WebDriver** – Browser automation
- ✅ **Python** – Core programming language
- ✅ **Pytest** – Test execution and fixtures
- ✅ **Allure** – Rich and interactive test reporting

---

## ✅ Features

- 🧱 **Page Object Model (POM)** design pattern for modular code
- 🪵 **Custom Logger** using Python's `logging` module
- 📸 **Automatic & Manual Screenshot Capture** on test failure and step-level validation
- 📊 **Allure Reporting** for each test run with step-wise breakdown
- 🌐 **Environment-Based Configuration** using YAML files (e.g., QA, DEV)
- 🔍 **Data-Driven Testing** via fixture parametrization
- 🔄 **Reusable Utility Methods** for cleaner test scripts
- 🧪 **Custom Pytest Hooks** for enhanced test control
- 📁 **Timestamped Reports & Screenshots** for each run
- 🧹 **Clean Folder Structure** for easy navigation and scalability

---

## 📁 Folder Structure

- `base/`           – Base classes like WebDriver setup, logger
- `configFiles/`    – Environment-based YAML config files
- `logs/`           – Stores log files for each test execution
- `pages/`          – Page Object Model classes
- `reports/`        – Allure reports saved with timestamps
- `screenshots/`    – Screenshots captured during execution
- `testcases/`      – Test scripts organized per module
- `testdata/`       – Test data (hardcoded or external)
- `utilities/`      – Helper methods (e.g., screenshot capture, YAML reader)
- `conftest.py`     – Pytest fixtures and hooks
- `pytest.ini`      – Pytest configuration file
- `requirements.txt` – List of dependencies
- `Runner.py`       – Entry point to run tests
- `setup.bat`       – Setup script for Windows
- `README.md`       – Project documentation

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Web_Automation_Framework(Py-PyTest).git
cd Web_Automation_Framework(Py-PyTest)
```
### 2. Run Setup Script (Windows)
```bash
Setup.bat
```
### 3. Manual Setup (Alternative)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Manual Setup (Alternative)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

# 🧪 Useful Commands

| Command                                | Description                              |
| -------------------------------------- | ---------------------------------------- |
| `pytest`                               | Run all test cases                       |
| `pytest -m smoke`                      | Run only smoke tests                     |
| `pytest --browser_name=chrome`         | Run with Chrome browser                  |
| `pytest --env=qa`                      | Load QA environment configs              |
| `pytest --alluredir=reports/allure-results` | Run tests and store Allure results     |
| `allure serve reports/allure-results`  | Launch Allure HTML report                |

---

# 👤 Author
**Ramanan Ramasamy**  
📍 Bengaluru, India  
🔗 https://www.linkedin.com/in/ramanan-ramasamy/  
💼 QA AUTOMATION Engineer | PYTHON | FULL STACK QA ENGINEER
