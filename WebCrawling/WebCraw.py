#Crowling
import requests
import openpyxl


from bs4 import BeautifulSoup
#csv 파일
def Craw(file,keyword):
    f = open(file+'.csv',"w")
    f.write('키워드,기사 제목,언론사\n')
    #str(n)기사 번호 즉 str(20)이면 20번째 기사 
    i = 1
    for i in range(1, 100, 10):
        url = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query="+ keyword +"&start="+str(i),
                            headers = {'User-Agent':'Mozilla/5.0'})
                            #headers  안티 크롤링 해제
        html = BeautifulSoup(url.text, 'html.parser')

    #컨테이너 수집
        articles = html.select("ul.type01>li")
    #기사별 데이터 수집
        for ar in articles:
            title = ar.select_one("a._sp_each_title").text
            source = ar.select_one("span._sp_each_source").text
            #print(title,source)

            #내용중 쉼표 제거
            title = title.replace(",","")
            source = source.replace(",","")
            source = source.replace("언론사 선정", "PiCK")
            #인코딩 문제 해결 
            title = title.replace(u'\xa0','')
            source = source.replace(u'\xa0','')
            title = title.replace(u'\u2027','')
            source = source.replace(u'\u2027','')


            #내용출력    

            f.write(keyword + ',' +title + ',' + source + '\n')



    f.close()


#엑셀파일
#파일불러오기 시도 파일 없으면 새로생성 
def Craw_xlsx(file,keyword):
    try:
        wb = openpyxl.load_Workbook(file+'.xlsx')
        sheet = wb.active
    except:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(['키워드','제목','언론사'])


    #keyword = input('명령어를 입력해주세요: ')

    for i in range(1,100,10):
        url = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&start="+str(i),
                            headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(url.text, "html.parser")
                    
        articles = html.select("ul.type01 > li")

        for ar in articles:
            
            title = ar.select_one("a._sp_each_title").text
            source = ar.select_one("span._sp_each_source").text
            

            source = source.replace("언론사 선정", "PiCK")

            sheet.append([keyword,title,source])

    wb.save(file+'.xlsx')


a = input("데이터를 저장할 파일 이름 : ")
b = input("크롤링 할 검색어 : ")
Craw(a,b)
#Craw_xlsx(a,b)