from django.shortcuts import render
from .forms import queryForm
from django.http import HttpResponse
from .helpers import scrap_data, init_driver
import pandas as pd 

# Create your views here.
def home(request): 
    return render(request,'gns/home.html')

def get_news(request): 
    if request.method == "POST": 
        form = queryForm(request.POST)
        if form.is_valid():
            # try : 
                res = pd.DataFrame()
                query_str = form.cleaned_data['query']
                queries_w_space = query_str.split(";")
                print(queries_w_space)
                queries = [x.strip() for x in queries_w_space]
                with init_driver() as driver: 
                    print("driver here")
                    for query in queries : 
                        if res.empty:
                            df = scrap_data(driver,query)
                            res = df
                            print("agus")
                            
                        else : 
                            df = scrap_data(driver,query)
                            res = pd.concat((res,df))
                            
                            print("tinus")
                    res.reset_index(drop=True,inplace=True)
                    res['date'] = res['date'].apply(lambda x : str(x))
                    response = HttpResponse(
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    filename="result.xlsx"
                    response["Content-Disposition"] = f"attachment;filename={filename}"
                    res.to_excel(response)
                    return response
            # except : 
            #         return HttpResponse("error after form validation")
        else : 
            return HttpResponse("error due to invalid form ")
                        


            