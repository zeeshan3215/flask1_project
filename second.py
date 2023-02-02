from distutils.log import debug
from fileinput import filename
from flask import * 
import easyocr
import re
from datetime import datetime,date
app = Flask(__name__)  
  
@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        reader = easyocr.Reader(['en']) 
        with open(f.filename, "rb") as f:
          img = f.read()
        result = reader.readtext(img,  detail = 0, paragraph=True)
        results="".join(result)
        
        CNIC_NO=re.findall(r'\d{5}[-]\d{7}[-]\d{1}', results)[0]

        DATE_OF_BIRTH= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[0]
        DATE_OF_BIRTH= DATE_OF_BIRTH.replace('.', '/',)
        datetime_object = datetime.strptime(DATE_OF_BIRTH, '%d/%m/%Y').date()
        DATE_OF_BIRTH=datetime_object.strftime("%m/%d/%Y")

        DATE_OF_ISSUE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[1]
        DATE_OF_ISSUE= DATE_OF_ISSUE.replace('.', '/',)
        datetimes_object = datetime.strptime(DATE_OF_ISSUE, '%d/%m/%Y').date()
        DATE_OF_ISSUE=datetimes_object.strftime("%m/%d/%Y")

        DATE_OF_EXPIRE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[2]
        DATE_OF_EXPIRE= DATE_OF_EXPIRE.replace('.', '/',)
        datetime_objects= datetime.strptime(DATE_OF_EXPIRE, '%d/%m/%Y').date()
        DATE_OF_EXPIRE=datetime_objects.strftime("%m/%d/%Y")

        TODAYs = date.today()
        TODAY=TODAYs.strftime("%m/%d/%Y")

        age=TODAYs - datetime_object
        if age.days<=8035:
            age="your age is under 22 years"
        else:
            age= "your age is over 22 years"   

        EXPIRE= datetime_objects - TODAYs
        if EXPIRE.days<=0:
            EXPIRE="your card is expire"
        else:
            EXPIRE= "their are "+ str(EXPIRE.days)+" days remaining to expire card"

        NAMES=  re.findall("[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", results)[0]
        FIRST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[0]
        LAST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[1]

        F_NAME=  re.findall("[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", results)[1]
        FIRST_NAME=  re.findall("[A-Z][a-z]+\S", F_NAME)[0]
        LAST_NAME=  re.findall("[A-Z][a-z]+\S", F_NAME)[1]
        if LAST_NAME==re.findall("[A-Z][a-z]+[L]", LAST_NAME)[0]:
         LAST_NAME= LAST_NAME[::-1]
         LAST_NAME= LAST_NAME.replace("L", '',1)
         LAST_NAME= LAST_NAME[::-1]

        #a=type(result)
        my_information = {'name': {'FIRST_NAME':FIRST_NAMES, 'LAST_NAME':LAST_NAMES }, 'cnic no.': CNIC_NO, 'Father name':  {'FIRST_NAME':FIRST_NAME, 'LAST_NAME':LAST_NAME }, 'Date of Birth': DATE_OF_BIRTH, 'Date of issue': DATE_OF_ISSUE, 'Date of expire': DATE_OF_EXPIRE, 'Today': TODAY, 'expire':EXPIRE, 'age': age }
        return render_template("response.html", name = my_information) 
       
  
if __name__ == '__main__':  
    app.run(debug=True) 