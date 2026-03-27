"""
Bing搜索工具 - 提供必应国内版搜索功能
"""

from typing import Dict

import requests
from bs4 import BeautifulSoup

from common.result import ApiResult


class BingSearchTool:
    """必应搜索工具类"""

    name = "bing_search"
    description = "必应国内版搜索，输入关键词，返回标题、链接、摘要，供Agent深度查询使用"

    def __init__(self, max_result_length=10000):
        self.base_url = "https://cn.bing.com/search"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Referer": "https://cn.bing.com",
            }
        )
        self.max_result_length = max_result_length

    def __call__(self, query: str) -> Dict:
        """调用搜索并返回结果字典"""
        return self.search(query).to_dict()

    def search(self, query: str) -> ApiResult:
        """执行搜索"""
        if not query or len(query.strip()) == 0:
            return ApiResult(code=-1, message="搜索关键词不能为空", data=None)

        try:
            params = {
                "q": query.strip(),
                "ensearch": "0"  # 强制中文必应
            }
            resp = self.session.get(self.base_url, params=params, timeout=15)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            results = self._parse_bing_results(soup)

            return ApiResult(
                code=0,
                message="Bing 搜索成功",
                data={
                    "query": query,
                    "results": results
                }
            )

        except Exception as e:
            return ApiResult(code=-1, message=f"搜索失败：{str(e)}", data=None)

    def _parse_bing_results(self, soup: BeautifulSoup):
        """解析 Bing 搜索结果：标题、链接、摘要"""
        results = []
        for item in soup.select(".b_algo"):
            try:
                title_elem = item.find("h2")
                link_elem = item.find("a")
                desc_elem = item.find("p")

                title = title_elem.get_text(strip=True) if title_elem else ""
                link = link_elem.get("href", "") if link_elem else ""
                desc = desc_elem.get_text(strip=True) if desc_elem else ""

                if title and link:
                    results.append({
                        "title": title,
                        "url": link,
                        "summary": desc
                    })
            except:
                continue

        return results[:10]  # 最多返回10条，防止超token


bing_search_tool = BingSearchTool()
