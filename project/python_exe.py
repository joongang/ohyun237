import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import webbrowser

def enter(event):
    global vol2, graphImage2
    vol.set(float(entry.get()))
    vol2 += vol.get()
    getDataAndGraph(vol2)
    graphImage2 = PhotoImage(file='graph.png', master=root)
    imageLabel.config(image=graphImage2)

def getDataAndGraph(vol2):
    global df
    df1 = pd.read_csv('sampleData.csv')
    lst = list(df1.iloc[-1])
    lst += [vol.get(), vol2]
    df.loc[len(df)] = lst

    plt.figure(figsize=(12,8))
    plt.subplot(3, 1, 1)
    plt.plot(df['totalAddedVol'], df['pH'])
    plt.ylabel('pH', fontdict={'size':15})
    plt.subplot(3, 1, 2)
    plt.plot(df['totalAddedVol'], df['temp'])
    plt.ylabel('Temperature', fontdict={'size':15})
    plt.subplot(3, 1, 3)
    plt.plot(df['totalAddedVol'], df['EC'])
    plt.xlabel('volume(mL)', fontdict={'size':15})
    plt.ylabel('Electrical conduction', fontdict={'size':15})
    plt.savefig('graph.png')

def calculate(n1, m1, v1, n2, v2):
    return n1*m1*v1/(n2*v2)

plt.figure(figsize=(12,8))
plt.subplot(3, 1, 1)
plt.plot([0], [0])
plt.ylabel('pH', fontdict={'size':15})
plt.subplot(3, 1, 2)
plt.plot([0], [0])
plt.ylabel('Temperature', fontdict={'size':15})
plt.subplot(3, 1, 3)
plt.plot([0], [0])
plt.xlabel('volume(mL)', fontdict={'size':15})
plt.ylabel('Electrical conduction', fontdict={'size':15})
plt.savefig('graph.png')

root = Tk()
root.geometry('2000x1200')

graphImage = PhotoImage(file='graph.png', master=root)
imageLabel = Label(root, image=graphImage)
label = Label(root, text='용액의 첨가량을 입력하세요')
entry = Entry(root)
button = Button(root, text='입력')
exitButton = Button(root, text='용액 첨가 종료', command=root.quit)
imageLabel.grid(row=1, column=1, sticky='w')
label.grid(row=1, column=2, sticky='w')
entry.grid(row=1, column=3, sticky='w')
button.grid(row=1, column=4, sticky='w')
exitButton.grid(row=2, column=3, sticky='n')

button.bind('<Button-1>', enter)
button.bind('<Return>', enter)

vol = DoubleVar()
vol2 = 0
df = pd.DataFrame(columns=['pH', 'temp', 'EC', 'addedVol', 'totalAddedVol'])

root.mainloop()

df.to_html('dataframe.html', justify='center')
file1 = open('index.html', 'r', encoding='utf-8')
file2 = open('index1.html', 'w')
file3 = open('dataframe.html', 'r', encoding='utf-8')
tlist = file1.read().split('"table">')
tdf = file3.read()
file2.write(tlist[0])
file2.write('"table">')
file2.write(tdf)
file2.write(tlist[1])
file1.close()
file2.close()
file3.close()

webbrowser.open_new_tab('index1.html')