
from flask import Flask, render_template, request
import pickle


app = Flask(__name__)

gr = pickle.load(open('gradient_booster_regressor_model ', 'rb'))
sc = pickle.load(open('standard_scalar ', 'rb'))    #we have to import strd scalar sc that is used during training amd testing the model

@app.route('/')
def man():
    return render_template('home.html') #render temp-opens the template


@app.route('/predict', methods=['POST'])    
def home():
    car = request.form['car']   #req the vals given by the user in html form
    age = request.form['age']
    kilometers_driven = request.form['kilometers_driven']   #similarly we r creating dummies as ML model (0,1)
    fuel_type = request.form['fuel_type']
    transmission = request.form['transmission']
    owner_type = request.form['owner_type']
    mileage = request.form['mileage']
    engine = request.form['engine']
    power = request.form['power']

    
    if (fuel_type == "1"):
        fuel_type_diesel = 0;
        fuel_type_lpg = 0;      
        fuel_type_petrol = 0;
        fuel = "CNG";           #written to print CNG as 000

    if (fuel_type == "2"):
        fuel_type_diesel = 1;
        fuel_type_lpg = 0;
        fuel_type_petrol = 0;
        fuel = "Diesel";

    if (fuel_type == "3"):
        fuel_type_diesel = 0;
        fuel_type_lpg = 1;
        fuel_type_petrol = 0;
        fuel = "LPG";

    if (fuel_type == "4"):
        fuel_type_diesel = 0;
        fuel_type_lpg = 0;
        fuel_type_petrol = 1;
        fuel = "Petrol";

    if (transmission == "1"):
        transmission_manual = 1;
        trans="Manual";
        
    if (transmission == "2"):
        transmission_manual = 0;
        trans="Automatic";

    if (owner_type == "1"):
        owner_type_second = 0;
        owner_type_third = 0;
        owner_type_fourth = 0;
        owner = "First";

    if (owner_type == "2"):
        owner_type_second = 1;
        owner_type_third = 0;
        owner_type_fourth = 0;
        owner = "second";

    if (owner_type == "3"):
        owner_type_second = 0;
        owner_type_third = 1;
        owner_type_fourth = 0;
        owner = "Third";

    if (owner_type == "4"):
        owner_type_second = 0;
        owner_type_third = 0;
        owner_type_fourth = 1;
        owner = "Fourth";           
                                    #standardizing the values of the model using strd scalar in an array

    result = sc.transform([[kilometers_driven,mileage,engine,power,age,fuel_type_diesel,fuel_type_lpg,fuel_type_petrol,transmission_manual,owner_type_fourth,owner_type_second,owner_type_third]])
    price = gr.predict(result)      #gr model price prediction in an array 
    print(price)

    #return jsonify(price[0])               #printing the only value present in an array as a final value
    return render_template('result1.html',price1 = price[0],car = car,age = age, kilometers_driven = kilometers_driven, fuel = fuel,trans = trans, owner=owner,mileage=mileage,engine=engine,power=power)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
