from base.base_class import BaseClass
from conftest import capture_screenshot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.wyystudy_login import Wangyiyun_login
from pages.wyy_search_page import WangyiyunSearchPage
from testdata.search_testdata import SearchTestData
from utilities.helpers import BrowserHelpers


class Test_WangYiYun_Search(BaseClass):

    def _do_login(self, load_config, logger):
        """登录网易云课堂，搜索用例的前置操作"""
        logger.info("前置：打开首页")
        self.driver.get(load_config['wyy_login_url'])

        BrowserHelpers.dismiss_privacy_popup(self.driver, logger)

        wy_lp = Wangyiyun_login(self.driver)

        # 点击登录按钮
        logger.info("前置：点击登录/注册按钮")
        login_btn = wy_lp.get_user_login_click()
        self.driver.execute_script("arguments[0].click();", login_btn)

        # 等待登录 iframe 加载
        logger.info("前置：等待登录弹窗 iframe 加载")
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

        # 输入账号密码
        logger.info("前置：输入账号密码")
        wy_lp.get_phonenumber_field().send_keys(load_config['email'])
        wy_lp.get_password_field().send_keys(load_config['password'])
        wy_lp.get_agree_concole().click()
        wy_lp.get_login_button().click()

        # 验证登录成功
        logger.info("前置：验证登录成功")
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#j-nav-login'))
        )
        logger.info(f"前置：登录成功，当前 URL: {self.driver.current_url}")

        

    # ==================== 精准搜索 ====================
    @pytest.mark.search
    @pytest.mark.parametrize("test_data", SearchTestData.exact_search)
    def test_search_exact(self, request, test_data, load_config, logger):
        logger.info("=== 用例：精准搜索 ===")
        self._do_login(load_config, logger)

        sp = WangyiyunSearchPage(self.driver)
        sp.switch_to_search_iframe()
        keyword = test_data["keyword"]
        logger.info(f"输入搜索关键词: {keyword}")
        sp.search(keyword)

        # 等结果页加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ykt-course-card'))
        )

        # 断言 1：页面跳转到搜索结果页
        assert sp.is_on_search_page(), f"未跳转到搜索结果页，当前 URL: {self.driver.current_url}"

        # 断言 2：URL 携带搜索关键词
        assert sp.has_keyword_in_url(keyword), f"URL 未包含搜索关键词，当前 URL: {self.driver.current_url}"

        # 断言 3：有搜索结果
        result_count = sp.get_result_count()
        assert result_count > 0, f"搜索结果为 0，期望至少 1 条"

        # 断言 4：前 3 条课程标题至少包含关键字中的部分词
        titles = sp.get_course_titles()[:3]
        logger.info(f"前 3 条课程标题: {titles}")
        assert len(titles) > 0, "未获取到课程标题"
        assert any("Python" in title for title in titles), \
            f"前 3 条标题中未包含 'Python' 相关课程，实际标题: {titles}"

        logger.info(f"精准搜索断言通过，共 {result_count} 门课程")
        capture_screenshot(request)

    # ==================== 模糊搜索 ====================
    @pytest.mark.search
    @pytest.mark.parametrize("test_data", SearchTestData.fuzzy_search)
    def test_search_fuzzy(self, request, test_data, load_config, logger):
        logger.info("=== 用例：模糊搜索 ===")
        self._do_login(load_config, logger)

        sp = WangyiyunSearchPage(self.driver)
        sp.switch_to_search_iframe()
        keyword = test_data["keyword"]
        logger.info(f"输入搜索关键词: {keyword}")
        sp.search(keyword)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ykt-course-card'))
        )

        # 断言 1：URL 包含关键词
        assert sp.has_keyword_in_url(keyword), f"URL 未包含搜索关键词"

        # 断言 2：有结果
        result_count = sp.get_result_count()
        assert result_count > 0, f"搜索结果为 0"

        # 断言 3：前 5 条标题中至少 3 条包含 Python
        titles = sp.get_course_titles()[:5]
        logger.info(f"前 5 条课程标题: {titles}")
        hit_count = sum(1 for t in titles if "python" in t.lower())
        assert hit_count >= 3, f"前 5 条中仅 {hit_count} 条包含 'python'，期望至少 3 条"

        logger.info(f"模糊搜索断言通过，前 5 条中 {hit_count} 条命中")
        capture_screenshot(request)

    # ==================== 空搜索 ====================
    @pytest.mark.search
    def test_search_empty(self, request, load_config, logger):
        logger.info("=== 用例：空搜索 ===")
        self._do_login(load_config, logger)

        sp = WangyiyunSearchPage(self.driver)
        sp.switch_to_search_iframe()
        logger.info("不输入内容，直接点击搜索按钮")
        sp.click_search()

        # 断言：未跳转到搜索结果页（URL 不包含 /courses-search）
        import time as _time
        _time.sleep(1)
        assert not sp.is_on_search_page(), \
            f"空搜索不应跳转到搜索结果页，当前 URL: {self.driver.current_url}"

        # 断言：搜索框仍然存在
        assert sp.get_search_input().is_displayed(), "搜索框未显示"

        logger.info("空搜索断言通过，未跳转")
        capture_screenshot(request)

    # ==================== 空格搜索 ====================
    @pytest.mark.search
    @pytest.mark.parametrize("test_data", SearchTestData.space_search)
    def test_search_space(self, request, test_data, load_config, logger):
        logger.info("=== 用例：空格搜索 ===")
        self._do_login(load_config, logger)

        sp = WangyiyunSearchPage(self.driver)
        sp.switch_to_search_iframe()
        logger.info(f"输入空格: '{test_data['keyword']}'")
        sp.search(test_data["keyword"])

        import time as _time
        _time.sleep(2)

        # 断言：页面不崩溃，无 500 错误
        page_text = self.driver.page_source[:1000]
        assert "500" not in page_text, "空格搜索导致服务器 500 错误"
        assert "服务器内部错误" not in page_text, "空格搜索导致服务器内部错误"

        logger.info(f"空格搜索断言通过，当前 URL: {self.driver.current_url}")
        capture_screenshot(request)
        #ux-modal > div.ux-modal_ft > span

    # ==================== 超长字符搜索 ====================
    @pytest.mark.search
    @pytest.mark.parametrize("test_data", SearchTestData.long_search)
    def test_search_long(self, request, test_data, load_config, logger):
        logger.info("=== 用例：超长字符搜索 ===")
        self._do_login(load_config, logger)

        sp = WangyiyunSearchPage(self.driver)
        sp.switch_to_search_iframe()
        keyword = test_data["keyword"]
        logger.info(f"输入 {len(keyword)} 个字符的超长搜索词")
        sp.search(keyword)

        import time as _time
        _time.sleep(2)

        # 断言：页面不崩溃
        page_text = self.driver.page_source[:1000]
        assert "500" not in page_text, "超长搜索导致服务器 500 错误"
        assert "服务器内部错误" not in page_text, "超长搜索导致服务器内部错误"

        logger.info(f"超长搜索断言通过，当前 URL: {self.driver.current_url}")
        capture_screenshot(request)
