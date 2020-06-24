import requests
from bs4 import BeautifulSoup
import csv
import datetime

def get_meta_section(url):
    section_name = ""
    ret_val = requests.get(url)
    page = ret_val.content
    page_soup = BeautifulSoup(page, 'html5lib')
    page_meta = page_soup.find("meta",attrs={'name':'sectionname'})
    section_name = page_meta["content"]
    return section_name

def get_meta_section_from_page(page_soup):
    page_meta = page_soup.find("meta",attrs={'name':'sectionname'})
    section_name = page_meta["content"]
    return section_name

def get_meta_keywords_from_page(page_soup):
    page_meta = page_soup.find("meta",attrs={'name':'keywords'})
    keywords = page_meta["content"]
    return keywords

def get_meta_keywords(url):
    ret_val = requests.get(url)
    page = ret_val.content
    page_soup = BeautifulSoup(page, 'html5lib')
    page_meta = page_soup.find("meta",attrs={'name':'keywords'})
    keywords = page_meta["content"]
    return keywords

def get_rows(url):
    result = []
    r1 = requests.get(url)
    status = "OK" if r1.status_code==200 else r1.status_code
    print("Request status:",status)

    # We'll save in coverpage the cover page content
    coverpage = r1.content
    # print("coverpage:",coverpage)

    # Soup creation
    soup1 = BeautifulSoup(coverpage, 'html5lib')

    # News identification
    coverpage_news = soup1.find_all("div", class_='article')
    print("Total news:",len(coverpage_news))
    verbose = False
    keywords = ["coronavirus","virus","corona","quarantine","isolation","disease","death","deaths","dies","die","dead","lockdown"]
    secondary_keywords = ["corona","coronavirus","virus","flu","fever","coughs","suspicious","suspected","cough","bangladeshi"]
    for cn in coverpage_news:
        items = [item for item in cn if str(item).strip()!='']
        news_title = cn.find('h3').get_text().strip()
        lower_news_title = news_title.lower()
        news_summary = " ".join([t.get_text().strip() for t in cn.find_all("p",class_="")])
        lower_news_summary = news_summary.lower()
        news_time = cn.find('p',class_="dateline").get_text().strip()
        news_link = cn.find('h3').find('a')["href"]
        news_details = ""

        r2 = requests.get(news_link)
        details_page = r2.content
        details_soup = BeautifulSoup(details_page, 'html5lib')

        news_keywords = get_meta_keywords_from_page(details_soup)
        lower_news_keywords = news_keywords.strip().lower()

        news_section = get_meta_section_from_page(details_soup).strip().lower()
        found = False
        for k in keywords:
            if (k in lower_news_keywords) or (k in lower_news_title):
                found = True
                break
        if found:
            print("news_title:",news_title)
            news_details = details_soup.find("div",class_="custombody").find_all("p")
            news_details = " ".join([t.get_text().strip() for t in news_details if t.get_text().strip()!=""])
            lower_news_details = news_details.lower()
            combined_news_text = lower_news_title+" "+lower_news_summary+" "+lower_news_details+" "+lower_news_keywords

            if news_section=="bangladesh":
                for sk in secondary_keywords:
                    if sk in combined_news_text:
                        result.append({"title":news_title,"time":news_time,"summary":news_summary,"details":news_details,"keywords":news_keywords})
                        # Only need to match one secondary keyword
                        break
        if verbose:
            print("news_summary:",news_summary)
            print("news_time:",news_time)
            print("news_link:",news_link)
            print("news_details:",news_details)
    return result


def create_article_dataset(csv_name,start_date):
    base_url = "https://bdnews24.com/archive/?date="
    with open(csv_name, mode='w') as csv_file:
        headers = ["title","time","summary","details","keywords"]
        writer = csv.DictWriter(csv_file,headers)
        writer.writeheader()
        
        print("Starting from:",start_date)
        for d in range(1000):
            current_date = start_date + datetime.timedelta(days=d)
            print("Date:",current_date)
            if current_date>datetime.date.today():
                break
            complete_url = base_url+str(current_date)
            print(complete_url)
            result = get_rows(complete_url)
            for r in result:
                writer.writerow(r)


if __name__=='__main__':
    # url definition
    url = "https://english.elpais.com/"
    url = "https://bdnews24.com/"
    url = "https://bdnews24.com/archive/?date=2020-03-01"

    csv_name = 'corona_flu_bd_article_with_meta.csv'
    start_date = datetime.date(2020,1,1)
    create_article_dataset(csv_name=csv_name,start_date=start_date)

    # collect data from beginning of year, and save to csv file
    # csv_name = 'corona_flu_bd_article.csv'
    # start_date = datetime.date(2020,1,1)
    # # create_article_dataset(csv_name=csv_name,start_date=start_date)

    # url = "https://bdnews24.com/bangladesh/2020/03/22/coronavirus-suspect-dies-in-sylhet-hospital"
    # section_name = get_mata_section(url=url)
    # print("Section name:",section_name)
    # keywords = get_meta_keywords(url)
    # print("Keywords:",keywords.lower())

