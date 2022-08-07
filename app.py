
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import logging
logging.basicConfig(filename= 'app.log', level= logging.INFO, format= '%(levelname)s %(asctime)s %(name)s %(message)s', )
app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    logging.info('Rendering HTML template.')
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            gre_score=float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if(is_research=='yes'):
                research=1
            else:
                research=0
            logging.info('Model input taken from the user.')

            # loading the model file from the storage
            filename = 'finalized_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb'))
            logging.info('Loaded the pickle file')

            # predictions using the loaded model file
            prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
            logging.info('Prediction phase executed successfully.')
            print('prediction is', prediction)
            # showing the prediction results in a UI
            logging.info('Final output displayed.')
            return render_template('results.html',prediction=round(100*prediction[0]))
        except Exception as e:
            logging.exception('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app