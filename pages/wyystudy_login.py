from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Wangyiyun_login:
    def __init__(self, driver):
        self.driver = driver

    _USER_LOGIN_CLICK = (By.CSS_SELECTOR, '#j-nav-login > span')
    _PHONENUMBER_FIELD = (By.CSS_SELECTOR, '#phoneipt')
    _PASSWORD_FIELD = (By.CSS_SELECTOR, '[placeholder="请输入密码"]')
    _AGREE_CONSOLE = (By.CLASS_NAME, 'dl-clause-login')
    _LOGIN_BUTTON = (By.CSS_SELECTOR, '#submitBtn')
    _ERROR_MESSAGE = (By.CLASS_NAME, 'ferrorhead')

    def get_user_login_click(self):
        return self.driver.find_element(*Wangyiyun_login._USER_LOGIN_CLICK)

    def switch_to_login_iframe(self):
        #iframe
        """遍历页面所有 iframe，找到包含手机号输入框的那个并切进去"""
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(iframe)
            try:
                self.driver.find_element(*Wangyiyun_login._PHONENUMBER_FIELD)
                return  # 找到了，留在当前 iframe 里
            except Exception:
                continue
        # 都没找到，回到主页面
        self.driver.switch_to.default_content()
        raise Exception("未找到包含登录表单的 iframe")

    def get_phonenumber_field(self):
        return self.driver.find_element(*Wangyiyun_login._PHONENUMBER_FIELD)

    def get_password_field(self):
        return self.driver.find_element(*Wangyiyun_login._PASSWORD_FIELD)

    def get_agree_concole(self):
        return self.driver.find_element(*Wangyiyun_login._AGREE_CONSOLE)

    def get_login_button(self):
        return self.driver.find_element(*Wangyiyun_login._LOGIN_BUTTON)

    def get_error_message(self):
        return self.driver.find_element(*Wangyiyun_login._ERROR_MESSAGE)
