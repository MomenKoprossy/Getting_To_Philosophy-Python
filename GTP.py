from bs4 import BeautifulSoup
import time, requests , re

#utility function to delete (), [] and whatever text between them
def prepText(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

def GTP(url,v):
    if(url == 'http://en.wikipedia.org/wiki/Philosophy'): #stopping condition
        print(url)
        return ('done')
    else:
        time.sleep(0.5) #to avoid heavy load on wiki as suggested
        res=requests.get(url)
        clean = prepText(res.text)
        bs = BeautifulSoup(clean, "html.parser") #clean text no parentheses
        bsd = BeautifulSoup(res.text, "html.parser") #full text incase the link inlcudes ()
        print(res.url)
        content =  bs.find('div', attrs={'class':'mw-parser-output'}) #main div where paragraphs exist
        p = content.findChildren('p',recursive=False) #gets only direct children
        for j,para in enumerate(p): #loop on each paragraph
            a = p[j].findChildren(href=re.compile('^/wiki/')) #check links with wiki ref
            if(a!=[]): #if the paragraph inlcudes links
                for i,link in enumerate(a): #check every link and gets it fully from untrimmed text
                    test0= bsd.find('div', attrs={'class':'mw-parser-output'})
                    test1=test0.findChildren('p',recursive=False)[j]
                    #print(test1)
                    test2=test1.findChild('a',href=re.compile('^'+a[i].get('href')))
                    nurl = 'http://en.wikipedia.org' + test2.get('href')
                    c = False
                    for k in v: #check incase this url was visited b4
                        if(nurl==k):
                            c = True
                    if(c== True):
                        continue
                    else:
                        v.append(nurl) #flag visited and call again till stop
                        if(a[i].get('href')!=None):
                            return GTP(nurl,v)
#testing the script ---> change range as you wish
count =0
for i in range(1):
    visited = ['']
    if(GTP('http://en.wikipedia.org/wiki/Special:Random',visited)=='done'):
        count+=1
print(count)
#failed text case for unknown reason all paragaphs gets trimmed despite the non existance of parentheses  
#GTP('https://en.wikipedia.org/wiki/Carbon_County,_Pennsylvania',visited)