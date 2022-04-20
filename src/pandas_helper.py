import pandas as pd
import matplotlib.pyplot as plt

def colInfo(col):
    len_Col = col.shape[0]
    num_zeroes = (col == 0).sum()
    num_missing = col.isna().sum()
    mean = 0
    median = 0
    uniques = len(col.unique())
    try:
        num_unknowns = ((col.str.lower() == 'unknown') | (
            col.str.lower() == ' ') | (col.str.lower() == '')).sum()
    except:
        num_unknowns = 0

    try:
        mean = col.mean()
        median = col.median()
    except:
        mean = 0
        median = 0

    data = [
        ['Zeroes',  f'{num_zeroes:,}',  f'{(num_zeroes/len_Col *100):.2f} %'],
        ['Missing', f'{num_missing:,}',  f'{(num_missing/len_Col *100):.2f} %'],
        ['Unknown', f'{num_unknowns:,}',
            f'{(num_unknowns/len_Col *100):.2f} %'],
        ['Uniques', f'{uniques:,}', f'{(uniques/len_Col *100):.2f} %'],
        ['Mean', f'{mean:.2f}', '-'],
        ['Median', f'{median:.2f}', '-'],
    ]
    
    info_table = pd.DataFrame(
        data, columns=['', 'Number', 'Percentage']).set_index('').style.set_caption("Table Info")
    display(info_table)
    
    vCountNum = col.value_counts()
    vCountPct = col.value_counts(normalize=True)*100
    vCountNum.name = 'Value Count'
    vCountPct.name = '% Value Count'
     
    value_count_table = pd.concat([vCountNum,vCountPct], axis=1)
    value_count_table = value_count_table.iloc[:10].style.set_caption("Top 10 Value Count Info")
    display(value_count_table)

    if col.dtype == 'float64':
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.plot(col)
        plt.axhline(y=mean, color='r', linestyle='-.', label='Mean')
        plt.axhline(y=median, color='b', linestyle='-.', label='Median')
        plt.title('Bar plot: '+col.name)
        plt.legend()
        plt.ylabel(col.name)

    elif col.dtype == 'int64':
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hist(col)
        plt.title('Histogram plot: '+col.name)
        plt.ylabel(col.name)
        
        if len(col.value_counts()) < 30:
            fig, ax = plt.subplots(figsize=(15, 8))
            col.value_counts().iloc[:10].plot(kind='bar')
            plt.title('Frequency of top 10: '+col.name)
            plt.ylabel(col.name)
    
    elif col.dtype == 'O':
        fig, ax = plt.subplots(figsize=(15, 8))
        col.value_counts().iloc[:10].plot(kind='bar')
        plt.title('Frequency of top 10: '+col.name)
        plt.ylabel(col.name)
        
        if len(col.value_counts()) > 15:
            fig, ax = plt.subplots(figsize=(15, 8))
            col.value_counts().iloc[-5:].plot(kind='bar')
            plt.title('Frequency of bottom 5: '+col.name)
            plt.ylabel(col.name)