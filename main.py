import requests
from bs4 import BeautifulSoup
import time

class UniversityRankingSpider:
    """中国大学排名爬虫类，实现翻页爬取功能"""
    def __init__(self, base_url, total_pages):
        self.base_url = base_url  # 排名页面基础URL
        self.total_pages = total_pages  # 总页数
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.universities = []  # 存储爬取的高校信息

    def get_page_data(self, page_num):
        """爬取单页的高校排名信息"""
        try:
            # 拼接带页码的URL（需根据实际网站的分页规则调整，此处为示例）
            url = f"{self.base_url}?page={page_num}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 抛出HTTP请求异常
            response.encoding = response.apparent_encoding  # 自动识别编码
            soup = BeautifulSoup(response.text, "html.parser")

            # 解析页面（需根据目标网站的HTML结构调整选择器，此处为通用示例）
            # 假设高校信息在class为"university-item"的标签中
            items = soup.select(".university-item")
            for item in items:
                try:
                    rank = item.select_one(".rank").text.strip()  # 排名
                    name = item.select_one(".name").text.strip()  # 校名
                    score = item.select_one(".score").text.strip()  # 得分
                    self.universities.append({"排名": rank, "学校名称": name, "总分": score})
                except Exception as e:
                    print(f"解析单条高校信息失败：{e}")
            print(f"第{page_num}页爬取完成，共获取{len(items)}所高校信息")
        except Exception as e:
            print(f"第{page_num}页爬取失败：{e}")

    def crawl(self):
        """执行翻页爬取主逻辑"""
        print("开始爬取中国大学排名信息...")
        for page in range(1, self.total_pages + 1):
            self.get_page_data(page)
            time.sleep(1)  # 延迟1秒，避免请求过快被反爬
        print(f"爬取完成！共获取{len(self.universities)}所高校的排名信息")

    def save_to_csv(self, filename="university_ranking.csv"):
        """将爬取的信息保存为CSV文件"""
        import csv
        if not self.universities:
            print("暂无数据可保存")
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.universities[0].keys())
            writer.writeheader()
            writer.writerows(self.universities)
        print(f"数据已保存至{filename}文件")

# 主程序执行
if __name__ == "__main__":
    # 注意：需替换为实际的中国大学排名网站基础URL和真实总页数
    # 此处仅为示例，需根据目标网站的分页规则调整
    BASE_URL = "https://example.com/university-ranking"  # 替换为真实排名网站URL
    TOTAL_PAGES = 20  # 替换为真实总页数（根据600所高校的分页情况调整）
    
    spider = UniversityRankingSpider(BASE_URL, TOTAL_PAGES)
    spider.crawl()
    spider.save_to_csv()# 在这里编写代码
