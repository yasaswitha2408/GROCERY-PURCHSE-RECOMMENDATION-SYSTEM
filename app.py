{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "5fffaf9e",
   "metadata": {},
   "outputs": [],
   "source": [
    "model = pickle.load(open(r'C:\\Users\\Sweety Chittineni\\Downloads\\grocery recommendation system\\rf_model.pkl', 'rb'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "dcc52d5f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__' (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      " * Restarting with watchdog (windowsapi)\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from flask import Flask, request, render_template\n",
    "import pickle\n",
    "from datetime import datetime\n",
    "\n",
    "# Initialize Flask app\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Load the trained RandomForest model and imputer\n",
    "model = pickle.load(open('rf_model.pkl', 'rb'))\n",
    "imputer = pickle.load(open('imputer.pkl', 'rb'))\n",
    "\n",
    "# Sample data for supplier recommendations (use your actual data source)\n",
    "suppliers = {\n",
    "    'apple': 'Supplier A',\n",
    "    'banana': 'Supplier B',\n",
    "    'milk': 'Supplier C'\n",
    "}\n",
    "\n",
    "@app.route('/')\n",
    "def home():\n",
    "    return render_template('index.html')\n",
    "\n",
    "@app.route('/predict', methods=['POST'])\n",
    "def predict():\n",
    "    try:\n",
    "        # Collecting form data\n",
    "        date = request.form['date']\n",
    "        temperature = float(request.form['temperature'])\n",
    "        humidity = float(request.form['humidity'])\n",
    "        event_attendance = int(request.form['event_attendance'])\n",
    "\n",
    "        # Convert the date to a datetime object\n",
    "        prediction_date = datetime.strptime(date, '%Y-%m-%d')\n",
    "\n",
    "        # Prepare the feature vector\n",
    "        input_features = np.array([[temperature, humidity, event_attendance]])\n",
    "\n",
    "        # Impute missing values if any (use the imputer)\n",
    "        input_features_imputed = imputer.transform(input_features)\n",
    "\n",
    "        # Predict using the trained model\n",
    "        prediction = model.predict(input_features_imputed)\n",
    "\n",
    "        # Get recommended groceries (this should be based on your model's logic)\n",
    "        recommended_groceries = get_grocery_recommendations(prediction)\n",
    "\n",
    "        # Return the prediction and recommendations to the user\n",
    "        return render_template('index.html', \n",
    "                               prediction_text=f\"Predicted grocery requirement for {prediction_date.strftime('%Y-%m-%d')}: {prediction[0]:.2f}\",\n",
    "                               recommended_groceries=recommended_groceries)\n",
    "    except Exception as e:\n",
    "        return render_template('index.html', prediction_text=f\"Error: {str(e)}\")\n",
    "\n",
    "# A function to recommend groceries based on prediction\n",
    "def get_grocery_recommendations(prediction):\n",
    "    recommended_groceries = []\n",
    "    grocery_items = ['apple', 'banana', 'milk']  # Example items, map to your actual items\n",
    "    for i, quantity in enumerate(prediction):\n",
    "        grocery_name = grocery_items[i]\n",
    "        supplier = suppliers.get(grocery_name, \"Unknown Supplier\")\n",
    "        recommended_groceries.append({\n",
    "            'name': grocery_name,\n",
    "            'quantity': quantity,\n",
    "            'supplier': supplier\n",
    "        })\n",
    "    \n",
    "    return recommended_groceries\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7648985b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
