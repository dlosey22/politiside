from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import difflib
from stop_words import get_stop_words
from time import sleep
# roadmap:
# add more sites
# use headless chrome instead of phantom.js
sw = get_stop_words('en')
print(len(sw))
print(sw[50:60])
wb = webdriver.PhantomJS(
    executable_path="C:\\Users\\danie\\Desktop\\politisides\\assets\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

css = """<style>
        body {
            width: 100%;
            height: 100%;
            background-color: whitesmoke;
        }
        .ps {
            background-color: whitesmoke;
            border: none;
            font-weight: bold;
            height: 100%;
            color: chocolate;
            font-size: 120%;
            width: 5%
        }
        .top {

            width: 101%;
            height: 75px;
            background-color: chocolate;
            position: fixed;
            top: 0px;
            left: 0px;
            z-index: 1000;
        }
        .menu {
            height: 100%;
            background-color: chocolate;
            border: none;
            font-size: 150%;

        }
        .menu:hover {
            transition-duration: .3s;
            color: whitesmoke;
        }
        .box {
            transition-delay: .2s;
            border-radius: 1%;
            width: 75%;
            width: 75%;
            height: 500px;
            background-color: navajowhite;
            margin-top: 1%;
            align-self: center;
            margin-left: 5%;
        }
        .box:hover {
            transition-duration: .5s;
            background-color: slategray;


        }
        .bottom {
            width: 100%;
            height: 20%;
            background-color: black;
            color: whitesmoke;

        }
        .symbol {
            text-align: center;
            vertical-align: bottom;
            padding-top: 6%;
        }
        img {

            position: relative;
            background-size: 100% auto;
            background-repeat: no-repeat;
            width: 45%;
            height: 50%;
            margin: 2.5%;
            margin-top: 2.5%;
        </style>
        }"""
def get_cnn():
    wb.get("https://www.cnn.com/")
    print("getting scource")
    html = wb.page_source
    soup = bs(html, "html.parser")

    hl = []
    links = soup.find_all("a", href=True)
    l = []
    for i in soup.find_all("span", class_="cd__headline-text"):
        if "https" not in str(i.parent) and "/2020":
            # print(str(i.parent))
            l.append("https://www.cnn.com" + i.parent["href"])
            i = str(i)

            headline = bs(i, "html.parser")
            headline = headline.text
            hl.append(headline)


    return hl, l


def get_fox():
    wb.get("https://www.foxnews.com/")
    html = wb.page_source
    soup = bs(html, "html.parser")
    articles = soup.find_all("a", href=True)
    l = []
    h = []
    for article in articles:
        if "foxnews.com/politics/" in str(article) and len(str(article.text)) > 5:
            l.append(article["href"])
            h.append(article.text)

    return h, l


def get_daily_wire():
    wb.get("https://www.dailywire.com/")
    html = wb.page_source
    soup = bs(html, "html.parser")
    articles = soup.find_all("a", href=True)  # attrs={"class" : "css-k008qs"}, href=True)
    h = []
    l = []

    for article in articles:
        if "Satire" not in str(article) and "/news/" in str(article["href"]):
            l.append("https://www.dailywire.com" + article["href"])
            h.append(article.text.split("By")[0])
    return h, l

def get_life_site_news():
    wb.get("https://www.lifesitenews.com/")
    html = wb.page_source
    soup = bs(html, "html.parser")
    a = soup.find_all("a", href = True)
    l = []
    h = []
    for i in a:
        if "/news/" in i["href"] and len(i.text)>20:
            l.append(i["href"])
            h.append(i.text)
    return h, l

def get_nbc():
    wb.get("https://www.nbcnews.com/")
    html = wb.page_source
    soup = bs(html, "html.parser")
    articles = soup.find_all("a", href=True)
    h = []
    l = []

    for article in articles:
        if "/news/us-news/" in str(article) and len(str(article.text).split(" ")) > 6:
            l.append(article["href"])
            h.append(article.text)
    #print(l)
    return h, l


def return_largest(l1, l2):
    a = len(l1)
    b = len(l2)
    if a > b:
        r1 = l1
        r2 = l2
    else:
        r1 = l2
        r2 = l1
    return r1, r2


def remove_sw(text):
    text_return = []
    for i in text.split(" "):
        if i not in sw:
            text_return.append(i)
    # text_return.pop(-1)
    text_return = " ".join(text_return)
    return text_return


def avg(lis):
    try:
        av = sum(lis) / len(lis)
    except ZeroDivisionError:
        print(lis)
        av = 0
    return av


def determine_matches(cnn, nbc, fox, wire, llinks, rlinks, thresh=43):
    cnn_nouns = []
    left = cnn + nbc
    right = fox + wire

    pairs = {}
    links = {}
    #if len(left) > len(right):
    #   print("right")
    avgl = []
    for i in right:
        for a in left:
            s1 = remove_sw(i.lower())
            s2 = remove_sw(a.lower())
            dif = difflib.SequenceMatcher(None, s1, s2).ratio() * 100
            avgl.append(dif)

            if dif > thresh:
                pairs.update({i: a})
                links.update({rlinks[right.index(i)]: llinks[left.index(a)]})


    step = 0

    return pairs, links




def make_site(articles, links):
    html = """<div class="box">

            <a href = target='_blank'><h1 class="left">{}</h1></a><a href = target='_blank'><h1 class="right">{}</h1></a>
            
        </div>
        """
    boxes = ''
    disqus = """        
        <div id="disqus_thread"></div>
        <script>

        /**
        *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
        *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
        /*
        var disqus_config = function () {
        this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
        };
        */
        (function() { // DON'T EDIT BELOW THIS LINE
        var d = document, s = d.createElement('script');
        s.src = 'https://politisides.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
        })();
        </script>
        <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>"""
    left = articles.values()
    llinks = iter(links.values())
    print(llinks)
    rright = list(articles.keys())
    right = iter(articles.keys())
    rlinks = iter(links.keys())
    print(rlinks)
    for i in list(left):
        try:
            box = html.format(i, next(right)).replace("href = ", 'href='+'"' + str(next(llinks))+'"', 1)
            box = box.replace("href = ", 'href='+'"'+str(next(rlinks))+'"', 1)
            with open("C:\\Users\\danie\\Desktop\\politisides\\home\\templates\\today.html", "rb") as file:
                if box not in file.read().decode("utf8"):
                    boxes = boxes + box #.replace("blah",disqus)
        except StopIteration:
            break
    with open("C:\\Users\\danie\\Desktop\\politisides\\home\\templates\\today.html", "rb+") as file:

        html = file.read()
        print(html)
        file.seek(0,0)
        html = html + boxes.encode("utf8")


        file.write(html)
        file.truncate()
def update_site(time):
    while 1:

        cnn = get_cnn()
        nbc = get_nbc()
        fox = get_fox()
        wire = get_daily_wire()
        pair, link = determine_matches(cnn[0], nbc[0], fox[0], wire[0], llinks=cnn[1]+nbc[1], rlinks=fox[1] + wire[1])
        make_site(pair, link)
        sleep(time)
update_site(120)

