import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://vladivostok.hh.ru/vacancies/kurer"
                  # ,"https://kazan.hh.ru/vacancies/kurer"
                  ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)

        # print('\n#######################\n%s\n#######################\n'%response.url)

    def parse_vacancy(self, response:HtmlResponse):
        vacancies_name = response.css('h1::text').get()
        vacancies_url = response.url
        vacancies_source = 'hh.ru'
        # vacancies_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        vacancies_salary = ''.join(response.xpath("//div[@data-qa='vacancy-salary']//text()").getall())
        if vacancies_salary:
            salary_list = vacancies_salary.split()
            if salary_list[0] == 'от':
                min_salary = int(salary_list[1] + salary_list[2])
                if salary_list[3] == 'до':
                    max_salary = int(salary_list[4] + salary_list[5])
                else:
                    max_salary = 'не указано'
            elif salary_list[0] == 'до':
                min_salary = 'не указано'
                max_salary = int(salary_list[1] + salary_list[2])
        else:
            min_salary = 'не указано'
            max_salary = 'не указано'
        yield ParserJobItem(
            name=vacancies_name,
            url=vacancies_url,
            salary_min=min_salary,
            salary_max=max_salary,
            source=vacancies_source
        )
