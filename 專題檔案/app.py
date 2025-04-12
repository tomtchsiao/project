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
    diet_calories = {
    'vegetarian': 1800,
    'meat': 2500,
    'lacto_ovo_vegetarian': 2000,
    'balanced': 2200
    }
    gain_or_lose = {
    'gain_weight': 1,
    'lose_fat': -1    
    }
    # 取得使用者輸入的數據
    data = request.json
    height = float(data['height'])
    weight = float(data['weight'])
    age = int(data['age'])
    gender = data.get('gender', 'male')
    activity_level = data.get('activityLevel', 'sedentary')
   # 取得飲食習慣和每日熱量攝取
    diet_type = data.get('dietType', 'balanced')
    gain_or_lose = data.get('goal', 'gain_weight')  # 預設值為 'gain_weight'
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
    if daily_calories <= 0 or Afterdays <= 0:
     return jsonify({'error': 'Invalid input values.'})
    daily_calorie_intake = diet_calories.get(diet_type, 2200)
    if gain_or_lose == 'gain_weight':
        daily_calorie_intake += 500  # 增重時增加 500 kcal
    elif gain_or_lose == 'lose_fat':
        daily_calorie_intake -= 500  # 減脂時減少 500 kcal
    # 計算目前體重變化
    calorie_deficit = daily_calorie_intake - daily_calories
    weight_change_per_day = calorie_deficit / 7700
    height_m = height / 100  # 將身高從公分轉換為公尺
    actual_weight = weight + weight_change_per_day * Afterdays  # 計算實際體重
    bmi = actual_weight / (height_m ** 2)
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
    'html': f"""
        <h2 style="text-align: center; color: #4CAF50; margin-bottom: 10px;">Analysis Results</h2>
        <table id="resultTable" style="width: 100%; border-collapse: collapse; margin-top: 20px; text-align: center;">
            <thead>
                <tr>
                    <th style="border: 1px solid #ddd; padding: 12px; background-color: #4CAF50; color: white;">Parameter</th>
                    <th style="border: 1px solid #ddd; padding: 12px; background-color: #4CAF50; color: white;">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 12px; font-weight: normal;">Actual Weight</td>
                    <td style="border: 1px solid #ddd; padding: 12px; font-weight: normal;">{actual_weight:.2f} kg</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 12px; font-weight: normal;">TDEE</td>
                    <td style="border: 1px solid #ddd; padding: 12px; font-weight: normal;">{tdee:.2f} kcal</td>
                </tr>
            </tbody>
        </table>
        <div class="suggestion" style="margin-top: 20px; text-align: center;">
            <strong>Suggestion:</strong> {suggestion}
        </div>
    """,
    'chartData': {
        'labels': list(calorie_data.keys()),
        'values': list(calorie_data.values())
    }
})
if __name__ == '__main__':
    app.run(debug=True)