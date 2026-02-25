import google.generativeai as genai
import os

# 🔑 Paste your Gemini API key here
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Text model
text_model = genai.GenerativeModel("gemini-2.5-flash")

# Vision model
vision_model = genai.GenerativeModel("gemini-2.5-flash")
def generate_workout(split_type, custom_muscle):

    splits = {
        "Single Muscle": """
Monday - Chest
Tuesday - Shoulder
Wednesday - Back
Thursday - Biceps
Friday - Triceps
Saturday - Leg
Sunday - Rest
""",
        "Double Muscle": """
Monday - Chest and Shoulder
Tuesday - Back and Biceps
Wednesday - Leg and Triceps
Thursday - Chest and Shoulder
Friday - Back and Biceps
Saturday - Leg and Triceps
Sunday - Rest
""",
        "Push Pull Legs": """
Monday - Chest, Shoulder and Triceps
Tuesday - Back and Biceps
Wednesday - Leg
Thursday - Chest, Shoulder and Triceps
Friday - Back and Biceps
Saturday - Leg
Sunday - Rest
"""
    }

    if split_type:
        prompt = f"""
Generate a detailed weekly workout plan based on this split:

{splits[split_type]}

For each day include:
- 4-5 exercises
- Sets and reps
- Beginner friendly
- Budget friendly (no advanced machines)
Format clearly day-wise.
"""
        response = text_model.generate_content(prompt)
        return response.text

    elif custom_muscle:
        prompt = f"""
Generate a detailed workout plan for {custom_muscle}.
Include:
- Warmup
- 6 exercises
- Sets and reps
- Tips for proper form
"""
        response = text_model.generate_content(prompt)
        return response.text

    return "Please select a split or enter a muscle."

def generate_meal_plan(goal, health_problem, food_pref, restrictions):

    prompt = f"""
Create a 7-day meal plan.

Goal: {goal}
Health Problems: {health_problem}
Preferred Foods: {food_pref}
Food Restrictions: {restrictions}

Make it:
- Student budget friendly
- Practical
- Include breakfast, lunch, dinner, snacks
- Mention estimated calories per day
- Mention approximate protein intake
Format clearly day-wise.
"""

    response = text_model.generate_content(prompt)
    return response.text

from PIL import Image

def analyze_meal(image):

    prompt = """
Analyze this food image and estimate:

- Food items present
- Calories (kcal)
- Protein (g)
- Carbs (g)
- Total fat (g)
- Cholesterol
- Additional nutritional notes

Give approximate values.
"""

    response = vision_model.generate_content([prompt, image])
    return response.text

import gradio as gr

with gr.Blocks(title="Personalized Workout & Diet Planner with AI") as app:

    gr.Markdown("# 🏋 Personalized Workout & Diet Planner with AI")

    with gr.Tab("Workout Routines"):

        split_dropdown = gr.Radio(
            ["Single Muscle", "Double Muscle", "Push Pull Legs"],
            label="Select Workout Split"
        )

        custom_input = gr.Textbox(
            placeholder="Want back muscle workout?",
            label="Custom Muscle Workout"
        )

        workout_output = gr.Textbox(lines=20, label="Generated Workout Plan")

        generate_btn = gr.Button("Generate Workout")

        generate_btn.click(
            generate_workout,
            inputs=[split_dropdown, custom_input],
            outputs=workout_output
        )

    with gr.Tab("Meal Planning"):

        goal = gr.Dropdown(
            ["Weight Loss", "Muscle Gain"],
            label="Goal"
        )

        health_problem = gr.Textbox(label="Health Problems")
        food_pref = gr.Textbox(label="Food Preference (Veg/Non-Veg + food names)")
        restrictions = gr.Textbox(label="Food Restrictions")

        meal_output = gr.Textbox(lines=20, label="Generated Meal Plan")

        submit_btn = gr.Button("Submit")

        submit_btn.click(
            generate_meal_plan,
            inputs=[goal, health_problem, food_pref, restrictions],
            outputs=meal_output
        )

    with gr.Tab("Meal Analysis"):

        image_input = gr.Image(type="pil", label="Upload Meal Image")
        analysis_output = gr.Textbox(lines=15, label="Nutritional Analysis")

        analyze_btn = gr.Button("Analyze Meal")

        analyze_btn.click(
            analyze_meal,
            inputs=image_input,
            outputs=analysis_output
        )

app.launch(server_name="0.0.0.0", server_port=7860)