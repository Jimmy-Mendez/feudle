import pandas as pd

data = pd.DataFrame(columns=['Question','Answer 1','#1','Answer 2','#2','Answer 3','#3','Answer 4','#4','Answer 5','#5','Answer 6','#6','Answer 7','#7'])
data_3_ans = pd.read_excel(open('quizzes.xlsx', 'rb'), sheet_name='3 Answers')  
data_4_ans = pd.read_excel(open('quizzes.xlsx', 'rb'), sheet_name='4 Answers')  
data_5_ans = pd.read_excel(open('quizzes.xlsx', 'rb'), sheet_name='5 Answers')  
data_6_ans = pd.read_excel(open('quizzes.xlsx', 'rb'), sheet_name='6 Answers')  
data_7_ans = pd.read_excel(open('quizzes.xlsx', 'rb'), sheet_name='7 Answers') 

data = pd.concat([data,data_3_ans,data_4_ans,data_5_ans,data_6_ans,data_7_ans])
data['Question'] = data['Question'].str.replace('’', '')
data['Question'] = data['Question'].str.replace('\"', '')
data['Question'] = data['Question'].str.replace(',', '')
data.to_csv('quizzes.csv',index=False)