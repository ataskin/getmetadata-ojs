import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# write metadata to excel without overwrite

def append_df_to_excel(df, excel_file):
    df_excel = pd.read_excel(excel_file)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_file, index=False)

with requests.Session() as s:
    i = 40
    while i < 50:
        # wait 5 seconds
        time.sleep(5)
        # the url is http://ojs.sbp.pl/index.php/pb/article/view/1 (2, 3, 4...) and increase
        url = 'http://ojs.sbp.pl/index.php/pb/article/view/' + str(i)
        r = s.get(url)

        if r.status_code == 200:
            soup = bs(r.content, 'lxml') # or 'html.parser'  - get content
            # find meta tags in HTML
            type = soup.find("meta",  {"name":"DC.Type.articleType"})
            if type != None:
                type = type["content"]
                # if type tag is set, collect the other metadata

                date = soup.find("meta",  {"name":"citation_date"})
                date = date["content"] if date else None

                titlepl = soup.find("meta",  {"name":"citation_title"})
                titlepl = titlepl["content"] if titlepl else None

                titleen = soup.find("meta",  {"name":"DC.Title.Alternative"})
                titleen = titleen["content"] if titleen else None

                author = soup.findAll(attrs={"name":"citation_author"})
                auth = " "
                for au in author:
                    auth = au["content"] + ", "+ auth

                journal = soup.find("meta",  {"name":"citation_journal_title"})
                journal = journal["content"] if journal else None

                affil = soup.find("meta",  {"name":"citation_author_institution"})
                affil = affil["content"] if affil else None

                abstr = soup.find("meta",  {"name":"DC.Description", "xml:lang":"en"})
                abstr = abstr["content"] if abstr else None

                volume = soup.find("meta",  {"name":"citation_volume"})
                volume = volume["content"] if volume else None

                issue = soup.find("meta",  {"name":"citation_issue"})
                issue = issue["content"] if issue else None

                doi = soup.find("meta",  {"name":"citation_doi"})
                doi = doi["content"] if doi else None

                pdflink = soup.find("meta",  {"name":"citation_pdf_url"})
                pdflink = pdflink["content"] if pdflink else None

                keywords = soup.findAll(attrs={"name":"DC.Subject", "xml:lang": "pl"})
                keywrd = " "
                for des in keywords:
                    keywrd = des["content"] + ", "+ keywrd

                # references are not listed as meta tag, so find them in <div> tags
                reference = soup.findAll('div',attrs={"id":"collapseCitations"})
                ref_tag = " "
                for ref in reference:
                    ref_tag = ref.text + " " + ref_tag
                # create metadata array
                metadata = [{'Type':type, 'Date':date, 'Title_PL':titlepl, 'Title_EN':titleen, 'Author':auth, 'Journal':journal, 'Affiliation':affil,
                             'Abstract':abstr, 'volume':volume, 'issue':issue, 'DOI':doi, 'Pdflink':pdflink, 'keywords':keywrd, 'References':ref_tag}]

                # set DataFrame
                df = pd.DataFrame(metadata)
                # call writing excel function
                # you must create the excel file manually before run the code
                append_df_to_excel(df, r"metadata.xlsx")
                print(url, ' OK')

            else:
                print(url, 'no content')
        else:
            print(url, r.status_code, ' not found ')
        # increase the number for url
        i += 1

