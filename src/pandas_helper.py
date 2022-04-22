import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score,cross_val_predict, cross_validate

# Color swatches
bToG = ['#0300c3', '#042492', '#053b83', '#055274', '#05616a',
          '#067a59', '#068c4d', '#07ad37', '#08c626', '#09ff00']
yToR = ['#fcb045', '#fc8439', '#fc5e2f', '#fc4227', '#fd1d1d']


def colInfo(col):
    """
    Helper function to print out information regarding a pandas Series (DataFrame column)
    
    col = pd.Series
    
    float: bar plot
    int: histogram plot
    object: bar plot of top 10 occurcences. If number of itmes > 15, plot additional bottom 5 occurences
    """
    len_Col = col.shape[0]
    num_zeroes = (col == 0).sum()
    num_missing = col.isna().sum()
    mean = 0
    median = 0
    uniques = len(col.unique())
    try:
        num_unknowns = (col.map(lambda x: x.lower() in ['unknown', ' ', '']).sum())
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
    
    info_table = pd.DataFrame(data, columns=['', 'Number', 'Percentage']).set_index('').style.set_caption("Table Info")
    
    #Creating Value Count Table
    vCountNum = col.value_counts()
    vCountPct = col.value_counts(normalize=True)*100
    vCountNum.name = 'Value Count'
    vCountPct.name = '% Value Count'
    
    #Limiting Table to top 10
    value_count_table = pd.concat([vCountNum,vCountPct], axis=1)
    value_count_table = value_count_table.iloc[:10].style.set_caption("Top 10 Value Count Info")
    
    # Display Tables as Panda DataFrames
    display(info_table,value_count_table)

    # Display plots depending upon datatype
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
            col.value_counts().iloc[:10].plot(kind='bar', color = bToG)
            plt.title('Frequency of top 10: '+col.name)
            plt.ylabel(col.name)
    
    elif col.dtype == 'O':
        fig, ax = plt.subplots(figsize=(15, 8))
        col.value_counts().iloc[:10].plot(kind='bar', color = bToG)
        plt.title('Frequency of top 10: '+col.name)
        plt.ylabel(col.name)
        
        if len(col.value_counts()) > 15:
            fig, ax = plt.subplots(figsize=(15, 8))
            col.value_counts().iloc[-5:].plot(kind='bar', color = yToR)
            plt.title('Frequency of bottom 5: '+col.name)
            plt.ylabel(col.name)
            
            
def modelReport(model, X, y,cv=True):
    '''
    Prints out cross validation test scoring metrics as a Pandas dataframe
    Displays a confusion matrix of the cross validation
    
    model = estimator to use for report generation
    X = input 
    y = output/label
    cv = Generates a cross validation report
    
    '''
    
    # Using cross_val_predict or model.predict to create a confusion matrix
    preds = cross_val_predict(estimator=model, X=X, y=y)  
        
    cm = confusion_matrix(y, preds, labels=model.classes_)
    disp = ConfusionMatrixDisplay(cm, display_labels=model.classes_)
    fig, ax = plt.subplots(figsize=(8, 8))
    disp.plot(cmap='OrRd', ax=ax)

    # Getting cross val scores
    getAllCrossValScores(model, X, y)


def getAllCrossValScores(model, X, y):
    '''
    Prints out cross validation test scoring metrics as a Pandas dataframe
    acc = Accuracy
    pr =  Precision (macro)
    re =  Recall (macro)
    f1 =  F1-score (macro)
    '''
    # Using cross_validate to generate accuracy, recall, precision and f1-scores
    cv = cross_validate(model, X, y, scoring=[
                        'accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])
    acc = cv['test_accuracy'].mean()
    pr = cv['test_precision_macro'].mean()
    re = cv['test_recall_macro'].mean()
    f1 = cv['test_f1_macro'].mean()

    data = [
        ['Accuracy',  f'{acc:.4f}'],
        ['Precision', f'{pr:.4f}'],
        ['Recall', f'{re:.4f}'],
        ['F1', f'{f1:.4f}'],
    ]

    info_table = pd.DataFrame(data, columns=['', 'Scores']).set_index(
        '').style.set_caption("Cross Validation Results")
    return(info_table)


def prettyPrintGridCVResults(GSCVModel):
    '''
    Tabulates results a grid search.
    Ranks by accuracy
    Shows all 4 mean test metrics: Accuracy, Precision Macro, Recall Macro, F1-score Macro
    Shows all parameters used for that model
    '''
    
    list_cols = ['rank_test_accuracy']
    list_metrics = ['mean_test_accuracy', 'mean_test_precision_macro',
                      'mean_test_recall_macro', 'mean_test_f1_macro']
    list_cols.extend(list_metrics)

    for col in GSCVModel.cv_results_.keys():
        if col.startswith('param_'):
            list_cols.append(col)
    
    


    table = pd.DataFrame(GSCVModel.cv_results_)
    for m in list_metrics:
        table[m] = table[m].map('{:,.4f}'.format)
    table = table[list_cols].sort_values(by='rank_test_accuracy')
    

        
    table.rename(columns={'rank_test_accuracy': 'Rank (By Accuracy)',
                          'mean_test_accuracy': 'Mean Test Accuracy',
                          'mean_test_precision_macro': 'Mean Test Precision (macro)',
                          'mean_test_recall_macro': 'Mean Test Recall (macro)',
                          'mean_test_f1_macro': 'Mean Test F1-Score (macro)'
                          }, inplace=True)
    

    return table.set_index('Rank (By Accuracy)')