#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, render_template, redirect , url_for,flash
import numpy as np
import pickle
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/work",methods=['POST'])
def work():
    if(request.form.get('action1') == 'Cancer'):
        return redirect(url_for('cancer'))
    elif(request.form.get('action2') == 'Heart disease'):
        return redirect(url_for('heart'))
    else:
        return render_template("FirstPage.html",result="i am error")
    


# In[2]:


model1 = pickle.load(open('cancerGB.pkl', 'rb'))
model2 = pickle.load(open('cancerSV.pkl', 'rb'))


@app.route('/cancer')
def cancer():
    return render_template('cancer.html')
@app.route('/predict', methods =['POST'])
def predict():
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    prediction1 = model1.predict(array_features)
    prediction2 = model2.predict(array_features)
    
    if(prediction1==prediction2=='High'):
        output = 2
    elif(prediction1==prediction2=='Low'):
        output = 0
    else:
        output = 1
    
    if(output == 1):
           return render_template("cancer.html",result="You have moderate chances of Cancer please visit a doctor")
    elif(output==2):
           return render_template("cancer.html",result="You have high chances of Cancer please visit a doctor urgently!")
    else:
        return redirect(url_for('external'))
@app.route('/external')             
def external():
    return render_template("external_cancer.html")
    
@app.route('/prediction', methods =['POST'])
def prediction():
    x=[]
    ind=[]
    flag=1
    li=[]
    
    switcher={
        0:'U have a past history may lead to cancer',
        1:'u have oxidative drug hsitory which may lead to cancer',
        2:'stop tobacco intake it is 33% effective in causing cancer',
        3:'take care of your diabeties 19% females and 27% males suffer from cancer due to diabeties'
    }
    phist=request.form.get('phist')
    dhist=request.form.get('dhist')
    tobac=request.form.get('tobacco')
    diab=request.form.get('diab')
    
    if(phist=='1'):
        x.append(1)
    else:
        x.append(0)
    if(dhist=='1'):
        x.append(1)
    else:
        x.append(0)
    if(tobac=='1'):
        x.append(1)
    else:
        x.append(0)
    if(diab=='1'):
        x.append(1)
    else:
        x.append(0)
    
    if(all(ele==1 for ele in x)):
        flag=1
    elif(all(ele==0 for ele in x)):
        flag=0
    else:
        flag=2
        
    if(flag==1):
        li.append("Though you dont have symptoms and other habbits but the external factors make you prone to cancer")
        li.append("Vist a doctor,just to be sure ")
    elif(flag==0):
        li.append("You are good to go,stay healthy!")
    else:
        for i in range(len(x)):
            if(x[i]==1):
                ind.append(i)
            else:
                continue
        li.append("Though you do not have symptoms but external factors suggest that you may have in future because")
        for i in ind:
            li.append(switcher.get(i,'invalid'))
        li.append("Get yourself checked")
    
    return render_template("external_cancer.html",result3=li)


# In[3]:


modela = pickle.load(open('modelGB.pkl', 'rb'))
modelb = pickle.load(open('modelSV.pkl', 'rb'))
modelc = pickle.load(open('modelDT.pkl', 'rb'))
modeld = pickle.load(open('modelGBC.pkl', 'rb'))

@app.route('/heart')
def heart():
    return render_template('heart disease classifier.html')



@app.route('/predict1', methods =['POST'])
def predict1():
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    prediction1 = modela.predict(array_features)
    prediction2 = modelb.predict(array_features)
    prediction3 = modelc.predict(array_features)
    prediction4 = modeld.predict(array_features)

    if(prediction1==prediction2==prediction3==prediction4==1):
        output = 1
    elif(prediction1==prediction2==prediction3==prediction4==0):
        output = 0
    else:
        if(prediction4==1):
            output=1
        else:
            output=0
                #flash("The paitent is likely to have heart disease")
                #return redirect(url_for('index'))
    
    if (output==1):
        return render_template("heart disease classifier.html",result="You are likely to have heart disease , consult a doctor")
    else:
        return redirect(url_for('index1'))
@app.route('/index1')             
def index1():
    return render_template("hdt.html")
    
@app.route('/prediction1', methods =['POST'])
def prediction1():
    x=[]
    flag=1
    ind=[]
    li=[]
    switcher={
        0:'TAke care of ur BMI',
        1:'U have a past history',
        2:'u have family hsitory',
        3:'take care of alchol',
        4:'stop smoking'
    }
    BMI = request.form.get('BMI')
    phist = request.form.get('phist')
    fhist = request.form.get('fhist')
    alchol = request.form.get('alcohol')
    smoke = request.form.get('smoke')
    if(BMI=='1'):
        x.append(1)
    else:
        x.append(0)
    if(phist=='1'):
        x.append(1) 
    else:
        x.append(0)
    if(fhist=='1'):
        x.append(1) 
    else:
        x.append(0)
    if(alchol=='1'):
        x.append(1) 
    else:
        x.append(0)
    if(smoke=='1'):
        x.append(1) 
    else:
        x.append(0)
    if(all(ele==1 for ele in x)):
        flag = 1
    elif(all(ele==0 for ele in x)):
        flag=0     
    else:
        flag=2
    if(flag==1):
        li.append("Though You dont have symtoms of heart diseases at present but external factors are postive and hence it increases the chances of heart disease")
        li.append("You may go to a  doctor")
    elif(flag==0):
        li.append("You are good")
        li.append("Stay healthy")
    else:
        li.append("Though you do not have symptoms but external factors suggest that you may have in future,hence")
        for i in range(len(x)):
                  if (x[i]==1):
                      ind.append(i)
        for i in ind:
                  s=(switcher.get(i,"invaild"))
                  li.append(s)
        li.append("Get yourself checked")
    return render_template("hdt.html",result3=li)


# In[ ]:


if __name__ == '__main__':
#Run the application
    app.run()


# In[ ]:





# In[ ]:




