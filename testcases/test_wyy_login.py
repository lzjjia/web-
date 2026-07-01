from base.base_class import BaseClass
from conftest import capture_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from pages.wyystudy_login import Wangyiyun_login
from utilities.helpers import BrowserHelpers

class Test_wangyyun(BaseClass):
    @pytest.mark.wangyiyun
    def test_screenScript(self, request, load_config, logger):
        logger.info(f"正在打开 {load_config['wyy_login_url']}")
        self.driver.get(load_config['wyy_login_url'])

        BrowserHelpers.dismiss_privacy_popup(self.driver, logger)

        logger.info("正在截图首页")
        capture_screenshot(request)
    @pytest.mark.wangyiyun
    def  test_login_success(self, request, load_config, logger):
        logger.info(f"正在打开 {load_config['wyy_login_url']}")
        self.driver.get(load_config['wyy_login_url'])

        BrowserHelpers.dismiss_privacy_popup(self.driver, logger)

        wy_lp = Wangyiyun_login(self.driver)

        # 第一步：点击首页右上角"登录/注册"按钮
        logger.info("第一步：点击登录/注册按钮（JS click）")
        login_btn = wy_lp.get_user_login_click()
        self.driver.execute_script("arguments[0].click();", login_btn)

        # 第二步：等弹窗 iframe 加载出来后切进去（最多等 10 秒，轮询尝试）
        logger.info("第二步：等待登录弹窗 iframe 加载")
        import time as _time
        switched = False
        for _ in range(20):
            _time.sleep(0.5)
            try:
                wy_lp.switch_to_login_iframe()
                switched = True
                break
            except Exception:
                pass
        if not switched:
            raise Exception("登录弹窗 iframe 在 10 秒内未加载")
        logger.info("已切换到登录 iframe")

        # 第二步：输入手机号
        logger.info("第二步：输入手机号")
        wy_lp.get_phonenumber_field().send_keys(load_config['email'])

        # 第三步：输入密码
        logger.info("第三步：输入密码")
        wy_lp.get_password_field().send_keys(load_config['password'])

        # 第四步：勾选同意协议
        logger.info("第四步：勾选同意协议")
        wy_lp.get_agree_concole().click()

        # 第五步：点击登录按钮
        logger.info("第五步：点击登录")
        wy_lp.get_login_button().click()

        # 断言：切回主页面，检查"登录/注册"按钮是否消失
        logger.info("断言登录结果")
        self.driver.switch_to.default_content()
        login_btn_gone = WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#j-nav-login'))
        )
        assert login_btn_gone, "登录失败：登录/注册按钮仍然可见，登录可能未成功"
        logger.info("断言通过：登录/注册按钮已消失，登录成功")

        logger.info("截图保存登录结果")
        capture_screenshot(request)
    def test_login_failed(self, request, load_config, logger):
        logger.info(f"正在打开 {load_config['wyy_login_url']}")
        self.driver.get(load_config['wyy_login_url'])

        BrowserHelpers.dismiss_privacy_popup(self.driver, logger)

        wy_lp = Wangyiyun_login(self.driver)

        # 第一步：点击首页右上角"登录/注册"按钮
        logger.info("第一步：点击登录/注册按钮（JS click）")
        login_btn = wy_lp.get_user_login_click()
        self.driver.execute_script("arguments[0].click();", login_btn)

        # 第二步：等弹窗 iframe 加载出来后切进去
        logger.info("第二步：等待登录弹窗 iframe 加载")
        import time as _time
        switched = False
        for _ in range(20):
            _time.sleep(0.5)
            try:
                wy_lp.switch_to_login_iframe()
                switched = True
                break
            except Exception:
                pass
        if not switched:
            raise Exception("登录弹窗 iframe 在 10 秒内未加载")
        logger.info("已切换到登录 iframe")

        # 第三步：输入手机号
        logger.info("第三步：输入手机号")
        wy_lp.get_phonenumber_field().send_keys(load_config['email'])

        # 第四步：输入错误密码
        logger.info("第四步：输入错误密码")
        wy_lp.get_password_field().send_keys('wrongpassword123')

        # 第五步：勾选同意协议
        logger.info("第五步：勾选同意协议")
        wy_lp.get_agree_concole().click()

        # 第六步：点击登录按钮
        logger.info("第六步：点击登录")
        wy_lp.get_login_button().click()

        # 断言：等待错误提示出现，验证提示文字内容
        logger.info("断言登录失败结果")
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ferrorhead'))
        )
        assert error_msg.text == "账号或密码错误", f"错误提示文字不匹配，实际内容: {error_msg.text}"
        logger.info("断言通过：出现'账号或密码错误'提示，登录失败符合预期")

        logger.info("截图保存登录失败结果")
        capture_screenshot(request)

        
        