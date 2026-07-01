from pages.saucelab_loginpage import SauselabLoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sauselab:

    @staticmethod
    def login(driver, username, password):
        lp = SauselabLoginPage(driver)
        lp.get_username_field().send_keys(username)
        lp.get_password_field().send_keys(password)
        lp.get_login_button().click()


class BrowserHelpers:

    @staticmethod
    def dismiss_privacy_popup(driver, logger, timeout=5):
        """关闭网易云课堂首页的隐私协议弹窗。存在即点掉，不存在跳过。"""
        try:
            btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#ux-modal > div.ux-modal_ft > span"))
            )
            btn.click()
            logger.info("已关闭用户协议弹窗")
        except Exception:
            logger.info("未出现用户协议弹窗，跳过")
            
