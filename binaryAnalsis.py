import io
import re
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import count
from DisplayTrajectories import getColoredLinesGraph
from openpyxl.drawing.image import Image

from Utils import time_performance, toBitStr, stripTrailingZeros, isGrowing

BINARYSTRINGSDIR = "BINARYSTRINGSDICT.json"

ANALSISEXCEL = "CollatzAnalysis.xlsx"

def collatzBinDerivative(userNum, fileSuffix = "", exportToCSV = True):#, formatFunc):
    n=userNum
    finalText = ""

    binStringsDictGlobal = {}
    
      
    binStringsList = [] #


    #df = pd.DataFrame(columns=("Number", "Bin","NextEvenBin","NextEvenBinReduced", "Reduction Size")) 
    d = {"Number":[], "Bin":[],"NextEvenBin":[],"NextEvenBinReduced":[], "Reduction Size":[], "diff":[],"pinPoint":[]} #,"Reduction Size":[], "Reductions By 
    

    newRow = {"Number":n, "Bin": toBitStr(n),
              "pinPoint": "Leap Start" if isGrowing(n) else ""}

    while n > 1 :

        binStringsList.append(newRow["Bin"])
        n = n * 3 + 1 
        
        newRow["NextEvenBin"] = toBitStr(n)
        newRow["NextEvenBinReduced"] =  newRow["NextEvenBin"].rstrip('0')

        newRow["Reduction Size"]= len(newRow["NextEvenBin"]) - len(newRow["NextEvenBinReduced"])
        
        n = int(newRow["NextEvenBinReduced"],2)
        newRow["diff"] = n - newRow["Number"]

        if isGrowing(n) and not isGrowing(newRow["Number"]):
            pinPointType = "Leap Start"
        elif not isGrowing(n) and isGrowing(newRow["Number"]):
            pinPointType = "    Peak"
        else:
            pinPointType = ""

        for k,v in newRow.items():
            d[k].append(v)
        #df = pd.concat([df, pd.DataFrame([newRow])], ignore_index=True)
        #print(df)
        
        newRow = {"Number":n, "Bin": newRow["NextEvenBinReduced"],"pinPoint":pinPointType }

            #dataRow[2] =toBitStr(n)
            #dataRow[3] = countLeadingZeros(dataRow[2])
            #finalText  = finalText+ "\n"# + formatBinNum(n) + "\n"
        #   printNum(n)
    else:
        df = pd.DataFrame(d)
        #df['derivative'] = df['Number'].diff()

        df['Reudction Power'] = 2 ** df["Reduction Size"]
       
        #print(df)

        redCountDF = pd.get_dummies(df['Reudction Power'], dtype = int).cumsum().add_prefix("Cnt Reduction By ")
        df["Leading Reduction"] = redCountDF.idxmax("columns")
        df = df.join(redCountDF)

        #if exportToCSV:
        #    df.to_csv(f"{userNum} analysis{fileSuffix}.csv")

        print(f"max number: {df["Number"].max()}" )
        #print(df)

        return df


def exportAnalysisToExcel(n,file_path = ANALSISEXCEL):
    sheetName = f"{n}"

    writer_kwargs = {
    "path": file_path,
    "engine": "openpyxl",
    "mode":"w",
    }

    if os.path.exists(file_path):
        writer_kwargs["if_sheet_exists"]="error"    
        writer_kwargs["mode"]="a"



    img_buffer = None

    with pd.ExcelWriter(**writer_kwargs) as writer: #, mode="a",if_sheet_exists="error") 
        wb = writer.book

        if sheetName not in wb.sheetnames:
                
            df = collatzBinDerivative(n, exportToCSV=False)
            #m = df["Number"].max()

            df.to_excel(writer,sheet_name= sheetName)
            ws = writer.sheets[sheetName]

            
            
            fig,ax = getColoredLinesGraph(n, toDisplay=False)
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format="png", bbox_inches="tight", dpi=150) #img_buffer
            img_buffer.seek(0)
            plt.close(fig)
            ws.add_image(Image(img_buffer), "S2")
        else: 
            print("already in file")
    
    if img_buffer:
        img_buffer.close()


def collatz_sequence(n, max_tries=None):
    """
    Generator that yields the Collatz sequence starting from n.
    If max_tries is provided, will stop after that many iterations.
    """
    tries = 0
    current = n
    
    while current != 1:
        yield current
        
        if max_tries and tries >= max_tries:
            break
            
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
            
        tries += 1
    
    yield current  # Yield the final 1



def gate_numbers(r):
    n = 262145 
    with pd.ExcelWriter("gate numbers.xlsx", engine="openpyxl") as writer:
        for i in range(r):
            #print(f"max number: {df["Number"].max()}" )
            df = collatzBinDerivative(n, exportToCSV=False)
            m = df["Number"].max()
            df.to_excel(writer,sheet_name= f"{n} {("dec" if m==n else "")}")
            n = 2 * n -1



@time_performance
def max_numbers(l):
    
    #df = pd.DataFrame(((i,toBitStr(max(collatz_sequence(i)))) for i in range(20,l)))
    nums = [0] * l # change to np array npzeros dtype 
    #nums = np.zeros(1_000_000_000, dtype=np.uint8)

    def get_collatz_stats(n):
        current = n
        max_val = n
        length = 1  # Accounts for the starting number (or final 1)

        while current != 1:
            if current < len(nums):
                if nums[current] == 1:
                    return n,max_val, f"{max_val:b}", length, current
                
                nums[current] = 1

            current = 3 * current + 1
           
            if current > max_val:
                max_val = current

            current = stripTrailingZeros(current)  #reduce all zeros

            length += 1

        return n,max_val, f"{max_val:b}", length, 1
    


    df = pd.DataFrame.from_records(( get_collatz_stats(i) for i in range(20,l) ),
    columns=['num', 'max','max_binary', 'length','part of'] 
    )
    df.to_csv(f"peaks analysisv2(20-{l}).csv", index=False)


#while True:
if __name__ == '__main__':
    #max_numbers(10000)

    #userNum = 97 
    userNum = int(input("Enter A Number: "),0)
    exportAnalysisToExcel(userNum)
    #time_performance(collatzBinDerivative)(userNum)

#time_performance(collatzBinDerivative2)(userNum)#userNum)





#print(allStructures(userNum))
