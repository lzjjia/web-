import inspect
import logging
import os
from datetime import datetime
import allure
import pytest
import yaml
from selenium import webdriver

driver = None

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Browser Selection")
    #报告存放目录
    parser.addoption("--run_folder", action="store", help="Folder where report/screenshots are stored")
    #截图存放目录
    parser.addoption("--screenshot_dir", action="store", help="Folder where screenshots are stored")
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests against: dev or qa")


#启动浏览器，这是fixture的前置操作，
# 在baseclass上被用到，后面继承的类，都可以使用这个作为一个前置操作，打开浏览器
@pytest.fixture()
def invokeBrowser(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    print(f"Browser name is {browser_name}")
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    #将浏览器窗口最大化显示
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()

#加载配置yaml配置文件，每个session只需要加载一次即可
@pytest.fixture(scope="session")
def load_config(request):
    """Load environment-specific configuration."""
    env = request.config.getoption("--env").lower()  # Get from CLI
    config_path = os.path.join(os.getcwd(), "configfiles", f"{env}_config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config
#失败自动截图
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot automatically on failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_instance = getattr(item.instance, "driver", None)
        if driver_instance:
            screenshot_folder = item.config.getoption("screenshot_dir")
            os.makedirs(screenshot_folder, exist_ok=True)

            test_method_name = item.name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{test_method_name}_failure_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_folder, filename)

            success = driver_instance.save_screenshot(screenshot_path)
            if success and os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as f:
                    allure.attach(f.read(), name=f"{test_method_name}_failure", attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    env = session.config.getoption("--env")
    with open("reports/environment.properties", "w") as f:
        f.write(f"Environment={env}\n")

def capture_screenshot(request):
    """Capture screenshot manually."""
    driver_instance = getattr(request.node.instance, "driver", None)
    if driver_instance:
        screenshot_folder = request.config.getoption("screenshot_dir")
        os.makedirs(screenshot_folder, exist_ok=True)

        test_method_name = request.node.name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{test_method_name}_manual_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_folder, filename)

        success = driver_instance.save_screenshot(screenshot_path)
        if success and os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as f:
                allure.attach(f.read(), name=f"{test_method_name}_Captured_screenshot", attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="session", autouse=True)
def configure_logger():
    testCaseName = inspect.stack()[1][3]
    logger = logging.getLogger(testCaseName)
    os.makedirs("logs", exist_ok=True)
    log_file_name = f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logger.log_path = f"logs/{log_file_name}"
    if not logger.handlers:
        fileHandler = logging.FileHandler(log_file_name, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.setLevel(logging.DEBUG)
    logging.root.logger = logger
    return logger


@pytest.fixture
def logger():
    testCaseName = inspect.stack()[1][3]
    return logging.getLogger(testCaseName)