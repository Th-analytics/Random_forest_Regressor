from flask import Flask, render_template, request, redirect, url_for
import threading
from math import floor
from eda import Predict
app = Flask(__name__)
global free_status, result_data
free_status = True
result_data = 'Processing'
obj = Predict()

class Threading:

    def __init__(self,object,values):
        self.object = object
        self.values = values
        thread = threading.Thread(target=self.run, args=())
        thread.daemon =True
        thread.start()

    def run(self):
        global free_status
        free_status = False
        threading.Thread(target=self.object.main(data=self.values)).start()
        free_status = True

# 'CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS','RAD','TAX','PTRATIO','BK','LSTAT'
@app.route('/', methods=['POST','GET'])
def home():
    global free_status

    if request.method == 'POST':
        if free_status != True:
            return "Website is Busy"
        else:
            free_status = True
        # Default Values
        if request.form['CRIM'] == '':
            data_values = [0.03237,0.0, 2.18, 0.0, 0.458, 6.998, 45.8, 6.0622,3.0, 222.0, 18.7, 394.63, 2.94]
        else:
            CRIM = float(request.form['CRIM'].strip())
            ZN= float(request.form['ZN'].strip())
            INDUS = float(request.form['INDUS'].strip())
            CHAS = float(request.form['CHAS'].strip())
            NOX = float(request.form['NOX'].strip())
            RM = float(request.form['RM'].strip())
            AGE = float(request.form['AGE'].strip())
            DIS = float(request.form['DIS'].strip())
            RAD = float(request.form['RAD'].strip())
            TAX = float(request.form['TAX'].strip())
            PTRATIO = float(request.form['PTRATIO'].strip())
            BK = float(request.form['BK'].strip())
            LSTAT = float(request.form['LSTAT'].strip())
            data_values = [CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATIO,BK,LSTAT]
        Threading(object=obj, values=data_values)
        return redirect(url_for('result'))
    else:
        return render_template('index.html')

@app.route('/result', methods = ['GET'])
def result():

    global result_data
    result_data = obj.result()
    if result_data != 'Processing...':
        result_data = floor(result_data)*1000
    print("result_data: ", result_data)
    return render_template('result.html', re_data = result_data)


if __name__=="__main__":

    app.run(port=8000,debug=True)