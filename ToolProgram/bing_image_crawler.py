# import the bingimagecrawler class from the icrawler.builtin module.
from icrawler.builtin import BingImageCrawler

# define a list of search words related to "chinese cabbage."
search_words = ["chinese cabbage"]

# specify the directory names for storing the downloaded images.
dir_names = ["chinese cabbage"]

# iterate over the pairs of search words and directory names using zip.
for search_word, dir_name in zip(search_words, dir_names):
    # create an instance of the bingimagecrawler class.
    bing_crawler = BingImageCrawler(
        downloader_threads=4,  # set the number of downloader threads to 4 for parallel downloading.
        storage={'root_dir': f"../recipedataset/{dir_name}"}  # set the root directory for storing images.
    )

    # initiate the image crawling process using bing search with the specified keyword and a maximum of 100 images.
    bing_crawler.crawl(
        keyword=search_word,
        max_num=100
    )