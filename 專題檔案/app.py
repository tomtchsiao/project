from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
# 計算基礎代謝率 (BMR)
def calculate_bmr(weight, height, age, gender):
    if gender == 'male':
        bmr = (9.99 * weight) + (6.25 * height) - (4.92 * age) + (166 * 1 - 161)
    else:
        bmr = (9.99 * weight) + (6.25 * height) - (4.92 * age) + (166 * 0 - 161)
    return bmr
# 計算每日總消耗熱量 (TDEE)
def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return bmr * activity_multipliers[activity_level]
# 根路由，返回首頁
@app.route('/')
def index():
    return render_template('index.html')
# 預測路由，處理表單提交
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    height = float(data['height'])
    weight = float(data['weight'])
    age = int(data['age'])
    gender = data.get('gender', 'male')
    activity_level = data.get('activityLevel', 'sedentary')
    diet_type = data.get('dietType', 'balanced')
    daily_calories = float(data['dailyCalories'])
    # 計算 BMR 和 TDEE
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    # 根據飲食習慣計算每日所需熱量
    diet_calories = {
        'vegetarian': 1800,
        'meat': 2500,
        'lacto_ovo_vegetarian': 2000,
        'balanced': 2200
    }
    Afterdays = int(data['Afterdays'])
    daily_calorie_intake = diet_calories.get(diet_type, 2200)
    # 計算目前體重變化
    calorie_deficit = daily_calorie_intake - daily_calories
    weight_change_per_day = calorie_deficit / 7700
    predicted_weight = weight + weight_change_per_day * Afterdays
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    # 提供使用者建議
    if bmi < 18.5:
        suggestion = "You are underweight. Consider increasing your calorie intake and doing strength training."
    elif 18.5 <= bmi < 24.9:
        suggestion = "You have a normal weight. Keep up your current diet and exercise habits."
    elif 25 <= bmi < 29.9:
        suggestion = "You are overweight. Consider reducing your calorie intake and increasing aerobic exercise."
    else:
        suggestion = "You are obese. Consult doctor and create a weight loss plan."
    calorie_data = {
        'Whole Grains': daily_calorie_intake * 0.3 / 70,
        'Beans, Fish, Eggs, Meat': daily_calorie_intake * 0.2 / 75,
        'Dairy': daily_calorie_intake * 0.15 / 150,
        'Vegetables': daily_calorie_intake * 0.2 / 100,
        'Fruits': daily_calorie_intake * 0.1 / 100,
        'Oils and Nuts': daily_calorie_intake * 0.05 / 45
    }
    # 回傳預測的體重和建議
    return jsonify({
        'predictedWeight': predicted_weight,
        'suggestion': suggestion,
        'BMR': bmr,
        'TDEE': tdee,
        'calorieData': calorie_data
    })
if __name__ == '__main__':
    app.run(debug=True)