import scrapy
import os

class StoriesSpider(scrapy.Spider):
    name = "stories"
    start_urls = [
        'https://yourstoryclub.com/story-category/short-stories-suspense-thriller/index.html',
        'https://yourstoryclub.com/story-category/short-stories-science-fiction/index.html',
        'https://yourstoryclub.com/story-category/editors-choice/index.html',
        'https://yourstoryclub.com/story-category/short-stories-funny/index.html',
        'https://yourstoryclub.com/story-category/short-stories-friendship/index.html',
        'https://yourstoryclub.com/story-category/short-stories-love/index.html',
        'https://yourstoryclub.com/story-category/short-stories-social-moral/index.html',
        'https://yourstoryclub.com/story-category/short-stories-family/index.html'
    ]

    def parse(self, response):
        for title_url in response.css('.entry-title a::attr(href)').getall():
            yield response.follow(title_url, callback=self.parse_story)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_story(self, response):
        story_text = ''

        for p in response.css('.entry-content p::text').getall():
            story_text += p.replace('\n', ' ')
            story_text += '\n\n'

        split_url = response.request.url.split('/')
        directory = split_url[-3]
        story_name = split_url[-2]

        file_path = directory + '/' + story_name + '.txt'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(story_text)
