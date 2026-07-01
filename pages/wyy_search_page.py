from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote


class WangyiyunSearchPage:

    def __init__(self, driver):
        self.driver = driver

    # 首页搜索框
    _SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-search="true"]')

    # 搜索结果页
    _RESULT_COUNT = (By.CSS_SELECTOR, '.j-result-count')
    _RESULT_KEYWORD = (By.CSS_SELECTOR, '.j-keyword')
    _COURSE_CARDS = (By.CSS_SELECTOR, '.ykt-course-card')
    _COURSE_TITLES = (By.CSS_SELECTOR, '.ykt-course-card_title_name')

    def switch_to_search_iframe(self):
        """遍历页面所有 iframe，找到包含搜索框的那个并切进去"""
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        print(f"[诊断] 共有 {len(iframes)} 个 iframe")
        for i, iframe in enumerate(iframes):
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(iframe)
            try:
                self.driver.find_element(*WangyiyunSearchPage._SEARCH_INPUT)
                print(f"[诊断] 在 iframe[{i}] 中找到搜索框")
                return
            except Exception:
                print(f"[诊断] iframe[{i}] 中找不到搜索框")
                continue
        # 都不在 iframe 里，在主页面找
        self.driver.switch_to.default_content()
        try:
            self.driver.find_element(*WangyiyunSearchPage._SEARCH_INPUT)
            print("[诊断] 在主页面中找到搜索框")
        except Exception:
            print("[诊断] 主页面中也找不到搜索框！")

    def get_search_input(self):
        return self.driver.find_element(*WangyiyunSearchPage._SEARCH_INPUT)

    def search(self, keyword):
        """输入关键词并回车搜索"""
        search_box = self.driver.find_element(*WangyiyunSearchPage._SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

    def click_search(self):
        """仅回车提交（用于空搜索，不输入内容直接搜索）"""
        search_box = self.driver.find_element(*WangyiyunSearchPage._SEARCH_INPUT)
        search_box.send_keys(Keys.RETURN)

    def get_result_count_text(self):
        """返回结果数量文字，如 '249'"""
        return self.driver.find_element(*WangyiyunSearchPage._RESULT_COUNT).text

    def get_result_count(self):
        """返回结果数量（整数）"""
        try:
            return int(self.get_result_count_text())
        except Exception:
            return 0

    def get_search_keyword(self):
        """返回搜索结果页显示的关键词"""
        return self.driver.find_element(*WangyiyunSearchPage._RESULT_KEYWORD).text

    def get_course_titles(self):
        """返回所有课程卡片标题的文本列表"""
        elements = self.driver.find_elements(*WangyiyunSearchPage._COURSE_TITLES)
        return [el.text for el in elements]

    def get_course_count(self):
        """返回当前页的课程卡片数量"""
        return len(self.driver.find_elements(*WangyiyunSearchPage._COURSE_CARDS))

    def has_keyword_in_url(self, keyword):
        """检查当前 URL（解码后）是否包含指定的关键词"""
        decoded_url = unquote(self.driver.current_url)
        return keyword.lower() in decoded_url.lower()

    def is_on_search_page(self):
        """判断当前是否在搜索结果页"""
        return '/courses-search' in self.driver.current_url
