import PreprocessModule as pm
import FeatureExtractionModule as fem
import ClusterModule as cm
import tkinter as tk
import bs4 as BeautifulSoup
import urllib.request
from fpdf import FPDF

def getOutputToFile():
    pdf = FPDF('L','mm','A4')
    pdf.add_page()
    pdf.set_font("Arial", size=25)
    pdf.cell(0,10,txt="SUMMARY",align="C")
    pdf.ln(h = '')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=summaryOutput.get("1.0",tk.END),align="C")
    pdf.output("output.pdf")
    pdf.close()
    

def onSummarizeClick():
    
    if(getVar1.get() == 1 and getVar2.get()==0):
        summaryOutput.delete(tk.END)
        file = open(location.get(),"r")
        dat = file.read()
        
    elif(getVar2.get() == 1 and getVar1.get()==0):
        fetched_data = urllib.request.urlopen(location.get())
        article_read = fetched_data.read()
        article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')
        paragraphs = article_parsed.find_all('p')
        dat=""
        for p in paragraphs:
            dat += p.text
    else:
        summaryOutput.insert(tk.END,"Choose a proper source")
        return 
        
    tobj = pm.TokenizeSentences(dat)
    tobj.getTokens()
    tobj.tokenizeWords(dat)
    prep = pm.Preprocess()
    ft = prep.filterDocument(tobj)
    fext = fem.SentenceScoring()
    fext.calculateScore(tobj,prep)
    score = fext.returnScore()
    clusterize = cm.MakeClusters()
    clusterize.formClusters(score)
    textSummary = clusterize.chooseSentences(score)
    summaryOutput.insert(tk.END,textSummary)

        

mainframe = tk.Tk(className='Text Summarizer')
mainframe.geometry("900x530")
mainframe.resizable(width=False, height=False)
bgimage = tk.PhotoImage(file='C:\\Users\\Vikky\\Desktop\\mini project\\Project development\\Final Code\\back4.png')
background_label = tk.Label(mainframe, image=bgimage)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
hlabel = tk.Label(mainframe,text="TEXT SUMMARIZER",bg='#a8326f',fg="yellow",font="Bahnschrift 36")
hlabel.pack()
label1 = tk.Label(mainframe,text="Please enter the loacation of local file or web page url",bg='#a8326f',fg="yellow",font="Bahnschrift 16")
label1.pack()
location = tk.StringVar()
textInput = tk.Entry(mainframe,width=100,font="Bahnschrift 15",textvariable=location)
textInput.pack()
label2 = tk.Label(mainframe,text="Please Choose a location",bg='#a8326f',fg="yellow",font="Bahnschrift 16")
label2.pack()
getVar1 = tk.IntVar()
getVar2 = tk.IntVar()
lfile = tk.Checkbutton(mainframe,text="Local Document        ",bg="#a8326f",font="Bahnschrift 12",variable=getVar1)
hfile = tk.Checkbutton(mainframe,text="HTML web resource",font="Bahnschrift 12",bg="#a8326f",variable=getVar2)
lfile.pack()
hfile.pack()
buttonCanvas=tk.Canvas(mainframe)
buttonCanvas.config(width=800,height=100)
buttonCanvas.pack()
summarize = tk.Button(buttonCanvas,text="Summarize",font="Bahnschrift 20",fg="black",bg="yellow",command=onSummarizeClick)
summarize.grid(row=0,column=1,rowspan=1)
getOp = tk.Button(buttonCanvas,text="Get Output To File",font="Bahnschrift 20",fg="black",bg="yellow",command=getOutputToFile)
getOp.grid(row=0,column=2,rowspan=1)
textCanvas = tk.Canvas(mainframe)
textCanvas.config(width=850,height=240,bg="black")
textCanvas.pack()
summaryop = tk.StringVar()
summaryOutput = tk.Text(textCanvas,bg="black",fg="white",font="Bahnschrift 12")
summaryOutput.place(x=0,y=0,height=240,width=850)
mainframe.mainloop()



        

    
    
