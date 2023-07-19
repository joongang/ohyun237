import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
    df1 = pd.read_csv('ard_sensor_daq_log.csv')
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

def granPlot(df):
    if df['pH'].iloc[0] < df['pH'].iloc[-1]:
        unknownAcidity = 1
    else:
        unknownAcidity = 0
    for i in range(len(df)):
        if unknownAcidity:
            if df['pH'].iloc[i] >= 7:
                VePoint = i
                break
        else:
            if df['pH'].iloc[i] <= 8:
                VePoint = i
                break
    Ve09 = df['totalAddedVol'].iloc[VePoint] * 0.9
    for i in range(len(df)):
        if unknownAcidity:
            if df['totalAddedVol'].iloc[i] >= Ve09:
                Ve09Point = i
                break
        else:
            if df['totalAddedVol'].iloc[i] <= Ve09:
                Ve09Point = i
                break
    filtered_df = df.iloc[Ve09Point:VePoint+1].copy()
    filtered_df.loc[:, ['Hdensity']] = filtered_df.loc[:, ['totalAddedVol']] * 10 ** (-filtered_df.loc[:, ['pH']])
    x = np.array(filtered_df['totalAddedVol'])
    y = np.array(filtered_df['Hdensity'])
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    return filtered_df, float(-model.intercept_[0]/model.coef_[0])

def granGraph(df, filtered_df, intercept):
    plt.figure(figsize=(12,8))
    plt.subplot(2, 1, 1)
    plt.plot(df['totalAddedVol'], df['pH'])
    plt.ylabel('pH', fontdict={'size':15})
    plt.xlabel('volume(mL)', fontdict={'size':15})
    plt.subplot(2, 1, 2)
    plt.plot(filtered_df['totalAddedVol'], filtered_df['Hdensity'])
    plt.ylabel('H density', fontdict={'size':15})
    plt.xlabel('volume(mL)', fontdict={'size':15})
    plt.text(intercept, 0, intercept, fontdict={'size':15, 'alpha':0.5})
    plt.savefig('grangraph.png')

def differentiate(df):
    df2 = df.iloc[:-1].copy()
    df2['differ'] = [0]*len(df2)
    for i in range(len(df2)):
        df2['differ'].iloc[i] = (df['pH'].iloc[i+1] - df['pH'].iloc[i]) / (df['totalAddedVol'].iloc[i+1] - df['totalAddedVol'].iloc[i])
    df3 = df2.iloc[:-1].copy()
    df3['differ2'] = [0]*len(df3)
    for i in range(len(df3)):
        df3['differ2'].iloc[i] = (df2['differ'].iloc[i+1] - df2['differ'].iloc[i]) / (df2['totalAddedVol'].iloc[i+1] - df2['totalAddedVol'].iloc[i])
    return df3

def differGraph(df):
    plt.figure(figsize=(12,8))
    plt.subplot(3, 1, 1)
    plt.plot(df['totalAddedVol'], df['pH'])
    plt.ylabel('pH', fontdict={'size':15})
    plt.subplot(3, 1, 2)
    plt.plot(df['totalAddedVol'], df['differ'])
    plt.ylabel('derivative', fontdict={'size':15})
    plt.subplot(3, 1, 3)
    plt.plot(df['totalAddedVol'], df['differ2'])
    plt.ylabel('second derivative', fontdict={'size':15})
    plt.xlabel('volume(mL)', fontdict={'size':15})
    plt.savefig('differgraph.png')

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
entry.bind('<Return>', enter)

vol = DoubleVar()
vol2 = 0
df = pd.DataFrame(columns=['pH', 'temp', 'EC', 'addedVol', 'totalAddedVol'])
df1 = pd.read_csv('ard_sensor_daq_log.csv')
lst = list(df1.iloc[-1])
lst += [0, 0]
df.loc[len(df)] = lst

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

granGraph(df, *granPlot(df))
differGraph(differentiate(df))

webbrowser.open_new_tab('index1.html')