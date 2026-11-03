""" & "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe" app.py
http://127.0.0.1:5000/predict
"""

from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)


def generate_recommendations(data):
    recommendations = []

    # 1. Attendance
    attendance = data["attendance_proxy_pct"]

    if attendance < 75:
        recommendations.append({
            "area": "Attendance",
            "status": "Needs Improvement",
            "message": (
                "Your attendance is relatively low. "
                "Try to attend classes regularly and catch up "
                "on lessons you missed."
            )
        })

    elif attendance < 90:
        recommendations.append({
            "area": "Attendance",
            "status": "Good",
            "message": (
                "Your attendance is reasonably good. "
                "Try to improve it further and maintain a "
                "consistent classroom routine."
            )
        })

    else:
        recommendations.append({
            "area": "Attendance",
            "status": "Excellent",
            "message": (
                "Your reported attendance is excellent. "
                "Maintain this consistency throughout the academic year."
            )
        })

    # 2. Study time
    study_time = data["studytime"]

    if study_time <= 1:
        recommendations.append({
            "area": "Study Time",
            "status": "Needs Improvement",
            "message": (
                "Consider setting aside more regular time for "
                "studying, revising lessons, and practicing questions."
            )
        })
    elif study_time == 2:
        recommendations.append({
            "area": "Study Time",
            "status": "Opportunity to Improve",
            "message": (
                "Try following a consistent study schedule, "
                "with focused revision and regular practice."
            )
        })
    else:
        recommendations.append({
            "area": "Study Time",
            "status": "Good",
            "message": (
                "Continue your study routine and focus on "
                "understanding concepts rather than memorizing."
            )
        })

    # 3. Previous grades
    g1 = data["G1"]
    g2 = data["G2"]

    if g2 < 10:
        recommendations.append({
            "area": "Previous Grades",
            "status": "Needs Improvement",
            "message": (
                "Your second-period grade is below 10/20. "
                "Review difficult topics, practice questions, "
                "and ask your teacher for guidance."
            )
        })
    elif g2 < 14:
        recommendations.append({
            "area": "Previous Grades",
            "status": "Opportunity to Improve",
            "message": (
                "Review the topics where you lost marks and "
                "practice similar questions before the next assessment."
            )
        })
    else:
        recommendations.append({
            "area": "Previous Grades",
            "status": "Good",
            "message": (
                "Your second-period grade is encouraging. "
                "Maintain your progress and revise regularly."
            )
        })

    if g2 < g1:
        recommendations.append({
            "area": "Recent Performance",
            "status": "Review Recommended",
            "message": (
                "Your second-period grade is lower than your first. "
                "Identify difficult topics and review what changed "
                "between the two assessments."
            )
        })
    elif g2 > g1:
        recommendations.append({
            "area": "Recent Performance",
            "status": "Improving",
            "message": (
                "Your grade improved between the two periods. "
                "Continue the study habits that are working for you."
            )
        })
    else:
        recommendations.append({
            "area": "Recent Performance",
            "status": "Stable",
            "message": (
                "Your grades are unchanged. Review your performance "
                "to identify opportunities for further improvement."
            )
        })

    # 4. Absences
    absences = data["absences"]

    if absences >= 10:
        recommendations.append({
            "area": "Absences",
            "status": "Needs Attention",
            "message": (
                "You reported a relatively high number of absences. "
                "Where possible, avoid unnecessary absences and "
                "catch up on missed coursework."
            )
        })
    elif absences >= 5:
        recommendations.append({
            "area": "Absences",
            "status": "Monitor",
            "message": (
                "Keep track of missed classes and make sure "
                "you complete any outstanding coursework."
            )
        })
    else:
        recommendations.append({
            "area": "Absences",
            "status": "Good",
            "message": (
                "Your reported absences are relatively low. "
                "Continue keeping up with lessons and coursework."
            )
        })

    return recommendations


# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load trained models
linear_regression_model = joblib.load(
    os.path.join(MODEL_DIR, "linear_regression.pkl")
)

random_forest_model = joblib.load(
    os.path.join(MODEL_DIR, "random_forest_regressor.pkl")
)

print("Regression models loaded successfully!")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Collect form inputs
        input_data = {
            "school": request.form["school"],
            "sex": request.form["sex"],
            "age": int(request.form["age"]),
            "address": request.form["address"],
            "famsize": request.form["famsize"],
            "Pstatus": request.form["Pstatus"],
            "Medu": int(request.form["Medu"]),
            "Fedu": int(request.form["Fedu"]),
            "Mjob": request.form["Mjob"],
            "Fjob": request.form["Fjob"],
            "reason": request.form["reason"],
            "guardian": request.form["guardian"],
            "traveltime": int(request.form["traveltime"]),
            "studytime": int(request.form["studytime"]),
            "failures": int(request.form["failures"]),
            "schoolsup": request.form["schoolsup"],
            "famsup": request.form["famsup"],
            "paid": request.form["paid"],
            "activities": request.form["activities"],
            "nursery": request.form["nursery"],
            "higher": request.form["higher"],
            "internet": request.form["internet"],
            "romantic": request.form["romantic"],
            "famrel": int(request.form["famrel"]),
            "freetime": int(request.form["freetime"]),
            "goout": int(request.form["goout"]),
            "Dalc": int(request.form["Dalc"]),
            "Walc": int(request.form["Walc"]),
            "health": int(request.form["health"]),
            "absences": int(request.form["absences"]),
            "G1": int(request.form["G1"]),
            "G2": int(request.form["G2"]),
            "subject": request.form["subject"],
            "attendance_proxy_pct": float(
                request.form["attendance_proxy_pct"]
            )
        }

        # Create DataFrame with the same feature order as training
        input_df = pd.DataFrame([input_data])

        # Generate predictions
        linear_prediction = float(
            linear_regression_model.predict(input_df)[0]
        )

        random_forest_prediction = float(
            random_forest_model.predict(input_df)[0]
        )

        # Keep predicted grades within the expected 0-20 range
        linear_prediction = max(0, min(20, linear_prediction))
        random_forest_prediction = max(0, min(20, random_forest_prediction))

        recommendations = generate_recommendations(input_data)

        return render_template(
        "index.html",
        linear_prediction=round(linear_prediction, 2),
        random_forest_prediction=round(random_forest_prediction, 2),
        input_data=input_data,
        recommendations=recommendations
    )

    except (ValueError, KeyError) as error:
        return render_template(
            "index.html",
            error_message=f"Please check your input values: {error}"
        ), 400

    except Exception:
        app.logger.exception("Prediction failed")

        return render_template(
            "index.html",
            error_message=(
                "Prediction failed. Please check the model files "
                "and input data."
            )
        ), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))