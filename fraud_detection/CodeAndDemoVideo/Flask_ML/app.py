from flask import Flask,render_template,request, redirect, url_for
import pickle
import numpy as np
# loading my mlr model
model=pickle.load(open('model.pkl','rb'))
#loading Scaler
scalar=pickle.load(open('scaler.pkl','rb'))

# Flask is used for creating your application
# render template is use for rendering the html page


app= Flask(__name__)  # your application


@app.route('/')  # default route 
def home():
    return render_template('home.html') # rendering if your home page.

@app.route('/pred',methods=['POST']) # prediction route
def predict():
    td= request.form["type"]
    ad = request.form["amount"]
    obo = request.form["oldbalanceOrg"]
    nbo = request.form["newbalanceOrg"]
    obd = request.form["oldbalanceDest"]
    nbd = request.form["newbalanceDest"]

    t =  [[float(td),float(ad),float(obo),float(nbo),float(obd),float(nbd)]]

    x=scalar.transform(t)
    output =model.predict(x)
    print(output)
    return redirect(url_for('result', result=np.round(output[0]))
@app.route('/result/<int:result>')
def result(result):
    if result == 0:
        result_class = "no-fraud"
        message = "No Fraudulent Transaction"
    else:
        result_class = "fraud"
        message = "Fraudulent Transaction!!!!!!"

    return render_template('result.html', result_class=result_class,result=message)
    
# running your application,
if __name__ == "__main__":
    app.run()

#http://localhost:5000/ or localhost:5000
