box_html = """<div class="box">
            <a href=""><img></a><a href=""><img></a>
        </div>"""


# print(box_html)

# give the ai a bunch of article return index of two that contradict.
def make_box(img1, img2, src1, src2, path):
    html = box_html
    im1 = """'""" + 'background-image: url({});'.format(img1) + """'"""
    im2 = """'""" + 'background-image: url({});'.format(img2) + """'"""
    html = html.replace("<img>", "<img style={}".format(im1), 1)
    html = html.replace("<img>", "<img style={}".format(im2), 1)
    html = html.replace('href=""', 'href="{}"'.format(src1), 1)
    html = html.replace('href=""', 'href="{}"'.format(src2), 1)
    with open(path, "r+") as file:
        a = file.read()
        a = a.replace("""<a id="starter"></a>""", '<a id="starter"></a>\n'+html)
        file.write(a)
    print(a)
    return html


make_box("1", "2", "1.c", "1.b", "C:/Users/danie/Desktop/politisides/home/templates/home.html")
