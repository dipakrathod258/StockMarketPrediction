import pandas as pd
import time
import os
from datetime import datetime

path = r"C:\Users\DEEPAK\Desktop\Backup\intraQuarter"

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
    statspath =  path+"/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]
    # print(stock_list)
    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'DE Ratio',
                               'Price',
                               'SP500',])
    sp500_df = pd.DataFrame.from_csv(r'C:\Users\DEEPAK\Downloads\^GSPC.csv')
    for each_dir in stock_list[1:]:
        each_file = os.listdir((each_dir))
        ticker = each_dir.split("\\")[-1]
        if len(each_file)>0:
            for file in each_file:
                date_stamp = datetime.strptime(file, "%Y%m%d%H%M%S.html")
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir+"/"+file
                source = open(full_file_path,'r').read()
                # print(source)
                try:
                    value = source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                    sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                    sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                    row = sp500_df[(sp500_df.index==sp500_date)]
                    sp500_value = float(row["Adj Close"])

                    stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]

                    df= df.append({'Date':date_stamp,
                                   'Unix':unix_time,
                                   'Ticker':ticker,
                                   'DE Ratio':value,
                                   'Price':stock_price,
                                   'SP500':sp500_value,
                                   }, ignore_index=True)
                    # print(df)
                except Exception as e:
                    pass

    save = gather.replace(' ','').replace('(','').replace(')','').replace('/','')+('.csv')
    # print(save)
    df.to_csv(save)

Key_Stats()