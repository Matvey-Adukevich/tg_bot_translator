from icrawler.builtin import GoogleImageCrawler

def parser_pictures(wordtofind):
	filters = dict(type='photo')
	crawler = GoogleImageCrawler(storage={'root_dir':'.'})
	crawler.crawl(keyword=wordtofind, max_num=1, overwrite=True, filters=filters)

# parser_pictures('sea')
