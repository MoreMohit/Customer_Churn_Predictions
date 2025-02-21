# #  Building a Flask API for Churn Explanations

# from flask import Flask,request,jsonify
# import google.generativeai as genai

# #Initialize Flask Name
# app = Flask(__name__)

# # Configure Gemini api-key
# genai.configure(api_key="AIzaSyBOgx6_jTZIZIsaE-Ol_awnKnyneHCtmSs")

# # Function to get ai powered churn explanations 

# def get_churn_explanation(features):
#     prompt = f"""
#     A customer is predicted to churn based on these factors: {features}.
#     Explain in a business-friendly way why they might leave and suggest a retention strategy.
#     """

#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt)
#     return response.text

# #API Route generate churn explanation
# @app.route('/', methods=['GET', 'POST'])
# def churn_explanation():
#     data = request.get_json()
#     return jsonify({"message": "Churn explanation received", "data": data})

#     # if not features:
#     #     return jsonify({"error":"No Features Provided"}),400
    
#     # explanation = get_churn_explanation(features)
#     # return jsonify({"churn_explanation":explanation})

# #Run the Flask App
# if __name__ == '__main__':
#     app.run(debug=True)
#     print(app.url_map)

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/churn_explanation', methods=['GET', 'POST'])
# def churn_explanation():
#      return jsonify({"message": "Use a POST request with JSON data."})
#     # data = request.json
#     # features = data.get("features", "")

#     # if not features:
#     #     return jsonify({"error": "No features provided"}), 400

#     # explanation = f"Simulated explanation for: {features}"  # Replace with AI logic
#     # return jsonify({"churn_explanation": explanation})

# if __name__ == '__main__':
#     app.run(debug=True)
# print("Available Routes:")
#print(app.url_map)


from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyBOgx6_jTZIZIsaE-Ol_awnKnyneHCtmSs")

# Function to get AI-powered churn explanations
def get_churn_explanation(features):
    prompt = f"""
    A customer is predicted to churn based on these factors: {features}.
    Explain why they might leave and suggest a retention strategy in a business-friendly way.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# API Route: Generate Churn Explanation
# @app.route('/', methods=['POST'])
# def churn_explanation():
#     data = request.json
#     features = data.get("features", "")

#     if not features:
#         return jsonify({"error": "No features provided"}), 400

#     explanation = get_churn_explanation(features)
#     return jsonify({"churn_explanation": explanation})

# Function to recommend retention strategies
def get_retention_strategy(features):
    strategies = []
    
    if "Low engagement" in features:
        strategies.append("Send a personalized re-engagement email with special offers.")
    if "High complaint rate" in features:
        strategies.append("Offer priority customer support and a free service upgrade.")
    if "Delayed payments" in features:
        strategies.append("Provide a flexible payment plan or temporary discount.")
    if "Competitor interest" in features:
        strategies.append("Give a limited-time discount or unique value proposition.")
    if "Subscription expiring soon" in features:
        strategies.append("Send a renewal reminder with a loyalty discount.")

    if not strategies:
        strategies.append("Maintain customer satisfaction with proactive engagement.")

    return strategies

@app.route('/', methods=['GET', 'POST'])
def churn_explanation():
    if request.method == 'GET':
        return jsonify({"message": "Use a POST request with JSON data to get churn explanations."})

    data = request.json
    features = data.get("features", "")

    if not features:
        return jsonify({"error": "No features provided"}), 400

    explanation = get_churn_explanation(features)
    return jsonify({"churn_explanation": explanation})

# API Route: Get Retention Recommendation
@app.route('/retention_strategy', methods=['GET', 'POST'])
def retention_strategy():

    
    if request.method == 'GET':
        return jsonify({"message": "Use a POST request with JSON data to get churn explanations."})
    
    data = request.json
    features = data.get("features", "")

    if not features:
        return jsonify({"error": "No features provided"}), 400

    strategy = get_retention_strategy(features)
    return jsonify({"retention_strategy": strategy})










# Run the Flask app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)


#curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/json" -d "{\"features\": \"Low engagement, high complaints\"}"