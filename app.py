from flask.views import MethodView
from wtforms import Form, StringField
from flask import Flask, render_template, request
from wtforms.fields.simple import SubmitField
from flatmates_bill.flat import Bill, Flatmate

app = Flask(__name__)



class BillFormPage(MethodView):
    """
    Creates a page containing a bill form object.
    Returns a html page to the user.
    Post request to gather data that has been inputted
    
    """

    def get(self):
        """
        Serves the bill form html page to the user.
        """
        bill_form = BillForm()
        return(render_template('bill_form_page.html', billform=bill_form))

    def post(self):
        """
        Gathers inputted data and calcualted the results
        """
        billform = BillForm(request.form)
        amount = billform.amount.data
        period = billform.period.data
        name1 = billform.name1.data
        days_in_house1 = billform.days_in_house1.data
        name2 = billform.name2.data
        days_in_house2 = billform.days_in_house2.data

        the_bill = Bill(float(amount), period)
        flatmate1 = Flatmate(name1, float(days_in_house1))
        flatmate2 = Flatmate(name2, float(days_in_house2))

        #return f"{flatmate1.name} pays {flatmate1.pays(the_bill, flatmate2)}"
        return(render_template('bill_form_page.html', result = True, 
         billform = billform, name1 = flatmate1.name,
         amount1 = flatmate1.pays(the_bill, flatmate2),
         name2 = flatmate2.name, amount2 = flatmate2.pays(the_bill, flatmate1)))



class BillForm(Form):
    """
    Class to create a Bill form to be served to the user.
    Contains all the input fields.
    """
    amount = StringField('Bill Amount: ')
    period = StringField('Bill Period: ')

    name1 = StringField('Name: ')
    days_in_house1 = StringField('Days In House: ')

    name2 = StringField('Name: ')
    days_in_house2 = StringField('Days In House: ')

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=BillFormPage.as_view('home_page'))
app.add_url_rule('/bill_form_page', 
view_func=BillFormPage.as_view('bill_form_page'))
#app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

#app.run(debug=True)