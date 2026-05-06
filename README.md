# Buffet Food Waste Prediction & Production Planning Dashboard

## 1. Project Overview

This project demonstrates how data science and machine learning can support buffet production planning and food waste reduction in hotel kitchen operations.

The project is inspired by my internship-based professional study on buffet production planning and leftover monitoring in a resort hotel kitchen. During the internship, I studied how buffet food waste may be reduced through better production planning, leftover recording, refill control, and pre-service communication.

The final output is a Streamlit dashboard that allows users to:

- Analyse buffet food waste patterns
- Identify high-risk dishes and kitchen sections
- Compare leftover ratios across meal periods and event types
- Predict whether a buffet item may become a high waste risk
- Generate operational recommendations for refill and production planning

## 2. Background and Problem Statement

In hotel buffet operations, kitchens often prepare and refill food based on experience rather than structured consumption data. This may lead to overproduction, unnecessary leftovers, and higher food costs.

The key operational problem is:

How can a hotel kitchen use data to monitor buffet leftovers, predict high waste risk, and support better production and refill decisions?

This project translates a hospitality and culinary management problem into a data science and machine learning project.

## 3. Dataset

The dataset used in this project is a synthetic operational dataset based on the structure of a leftover monitoring sheet proposed in my internship report.

The dataset contains 500 buffet operation records and includes the following fields:

- date
- weekday
- meal_period
- dish_name
- dish_category
- kitchen_section
- estimated_guests
- actual_guests
- event_type
- occupancy_rate
- weather
- prepared_qty
- leftover_qty
- leftover_ratio
- service_time_remaining
- refill_count
- waste_level
- possible_reason
- recommended_action

The dataset is simulated for academic and portfolio purposes. However, the data structure is based on a realistic hotel buffet operation scenario observed during my internship.

## 4. Methods and Tools

- Python
- pandas
- NumPy
- matplotlib
- Plotly
- scikit-learn
- Random Forest Classifier
- Streamlit
- GitHub

## 5. Exploratory Data Analysis

The analysis showed that Cold Dishes and Cold / Prep had the highest average leftover ratios. This suggests that cold dishes, side toppings, and pre-prepared items may require closer monitoring, smaller batch preparation, and more careful refill decisions near the end of service.

Lunch and dinner showed slightly higher leftover ratios than breakfast, but the difference was relatively small. This suggests that food waste reduction should not focus only on one meal period.

Normal buffet service showed a higher average leftover ratio than banquet, group tour, and wedding events. This may be because event-based services usually have clearer guest numbers, while normal buffet service has less predictable demand.

## 6. Machine Learning Model

The project includes a binary classification model that predicts whether a buffet item is a high waste risk.

Target variable:

- 1 = High Waste Risk
- 0 = Not High Waste Risk

The final high waste risk model achieved:

- Accuracy: 0.6800
- Precision: 0.5122
- Recall: 0.6364
- F1-score: 0.5676
- ROC-AUC: 0.7363

In this operational context, recall is important because the system should identify as many high waste risk cases as possible.

## 7. Dashboard Features

The Streamlit dashboard contains three main sections:

### Overview

This section displays:

- Total number of records
- Average leftover ratio
- Number of high waste records
- Average occupancy rate
- Sample data table
- Waste level distribution

### Waste Analysis

This section visualises:

- Top dishes by average leftover ratio
- Waste by kitchen section
- Waste by meal period
- Waste by event type

### High Waste Risk Prediction

This section allows users to input operational conditions such as meal period, dish category, kitchen section, event type, weather, estimated guests, occupancy rate, prepared quantity, service time remaining, and refill count.

The system then outputs:

- High waste risk probability
- Prediction result
- Operational recommendation
- Model input summary

## 8. Example Prediction

Example input:

- Meal Period: Dinner
- Dish Category: cold dish
- Kitchen Section: Cold Dishes
- Event Type: normal
- Weather: rainy
- Estimated Guests: 90
- Occupancy Rate: 0.55
- Prepared Quantity: 10
- Service Time Remaining: 15 minutes
- Refill Count: 3

Example output:

- High Waste Risk Probability: 80.92%
- Prediction: High Waste Risk

Operational recommendation:

The system recommends reducing initial production quantity, avoiding large final refills, and reviewing the item in the next weekly production meeting.

## 9. Operational Value

This project shows how data science can support hospitality operations in several ways:

1. It converts daily buffet operations into structured data.
2. It identifies dishes and kitchen sections with higher leftover risk.
3. It supports more informed production planning.
4. It provides refill recommendations based on risk level and service timing.
5. It connects culinary management knowledge with data science and machine learning methods.

## 10. Limitations

This project has several limitations:

- The dataset is synthetic and should be replaced with real operational data in a real hotel setting.
- Guest preference, food quality, pricing, and menu rotation are not fully included.
- The current model is a prototype and should be validated with real buffet service records.
- The recommendation logic is simplified and should be reviewed by kitchen supervisors before practical implementation.

## 11. Future Improvements

Future versions of this project may include:

- Real hotel buffet operation data
- More detailed dish-level consumption records
- Time-series demand forecasting
- Cost estimation for food waste
- Integration with inventory and purchasing data
- More advanced machine learning models
- A more interactive production planning module

## 12. Relevance to My Graduate Study Direction

This project reflects my transition from Culinary Management to Data Science and Artificial Intelligence.

My undergraduate background provided me with domain knowledge in foodservice operations, kitchen workflow, food safety, sensory evaluation, product development, and hospitality business management.

Through this project, I applied Python, data analysis, machine learning, and dashboard development to address a real operational issue in buffet food waste reduction.

This project supports my interest in applying data science and AI to hospitality operations, foodservice analytics, menu intelligence, demand forecasting, and sustainable kitchen management.
