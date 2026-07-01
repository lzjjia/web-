class SearchTestData:
    """搜索场景测试数据"""

    exact_search = [{"keyword": "Python自动化测试"}]

    fuzzy_search = [{"keyword": "python"}]

    empty_search = [{"keyword": ""}]

    space_search = [{"keyword": "   "}]

    long_search = [{"keyword": "测" * 500}]
