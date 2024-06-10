from flask import *
import os
from werkzeug.utils import secure_filename
import label_image
import PreProcessing

def load_image(image):
    text = label_image.main(image)
    return text

app = Flask(__name__)

pp = PreProcessing
@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')

 
  
    
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/index1')
def index1():
    #return "Index Page"
    return render_template('index1.html')

@app.route('/',methods = ['POST'])
def result():
    grains = request.form['grains']
    vegetables = request.form['vegetables']
    fruits = request.form['fruits']
    protein = request.form['protein']
    grains = float(grains)
    vegetables = float(vegetables)
    fruits = float(fruits)
    protein = float(protein)
    predictedResult = pp.healthy_diet(grains,vegetables,fruits,protein)
    print('Experience is ',predictedResult)
    predictedResult1 = pp.protein_diet(grains,vegetables,fruits,protein)
    print('Experience is ',predictedResult1)
    predictedResult2 = pp.grains_diet(grains,vegetables,fruits,protein)
    print('Experience is ',predictedResult2)    
    predictedResult3 = pp.vegetables_diet(grains,vegetables,fruits,protein)
    print('Experience is ',predictedResult3)    
    return render_template('result.html', PredictedResult = predictedResult,PredictedResult1 = predictedResult1,PredictedResult2 = predictedResult2,PredictedResult3 = predictedResult3,)

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        # Make prediction
        result = load_image(file_path)
        d = d = {"Chicken Curry": "→ Nutrition Data per 100g serving - Protein 12g, Carbs 3.2g, Fat 5.2g, Fiber 1.1g Calories 108kcal",
                 'Fried Rice': "→ Nutrition Data per cup (200g) serving - Protein 4g, Carbs 40g, Fat 6.8g, Fiber 1.6g Calories 220kcal","Dosa": "→ Nutrition Data per dosa (2-3 pcs, 100g) - Protein 4g, Carbs 20-30g, Fat 6.8g, Fiber 1.6g Calories 220kcal (varies with size)",
                 "Chicken Briyani": "→ Nutrition Data per cup (200g) serving - Protein 16g, Carbs 40g, Fat 10.4g, Fiber 1.6g Calories 300kcal",
                 "Rice (Basmati)": "→ Nutrition Data per cup (185g) cooked - Protein 5g, Carbs 45g, Fat 0.3g, Fiber 0.6g Calories 205kcal","Vada": "→ Nutrition Data per vada (2 pcs, 100g) - Protein 4g, Carbs 20g, Fat 6.8g, Fiber 1.6g Calories 220kcal (varies with size)",
                 "Poori": "→ Nutrition Data per poori (2 pcs, 100g) - Protein 4g, Carbs 20g, Fat 10.4g, Fiber 1.6g Calories 280kcal (varies with size)",
                 "Idly": "→ Nutrition Data per 2 idlies (100g) - Protein 8.1g, Carbs 46.2g, Fat 13.4g, Fiber 7.8g Calories 335kcal"
}

       
        # Add your response based on the result
        if "Image cannot be recognized." in result:
            response = result
        else:
            response = f"{result+d[result]}"

        os.remove(file_path)
        return response

    return None

if __name__ == '__main__':
    app.run()