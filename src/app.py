from flask import Flask, request, send_from_directory, jsonify
import sparknlp
import db_client
import prediction_services

app = Flask(__name__)

# spark needs to initialized outside of flask app because it needs to run outside of
# python worker threads and flask creates workers to serve requests
spark = sparknlp.start()
prediction_services_obj = prediction_services.Predictor(spark)


@app.route("/predict", methods=["POST"])
def process_question():
    # Extract the question text from the JSON payload
    question_text = request.json["question_text"]
    prediction = prediction_services_obj.predict(question_text)
    db_client.save_question(question_text, prediction)
    return "", 204


@app.route("/questions")
def get_questions():
    json_docs = db_client.get_recent_questions()
    return jsonify(json_docs)


@app.route('/web/<path:path>')
def send_static(path):
    return send_from_directory('../web', path)


if __name__ == "__main__":
    app.run(debug=False)
