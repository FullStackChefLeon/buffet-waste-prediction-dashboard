# Project Brief  
## Buffet Food Waste Prediction & Production Planning Dashboard

### 1. Project Background

This project was developed based on a resort hotel buffet kitchen operation scenario. During my internship, I studied how buffet food waste could be reduced through better production planning, leftover monitoring, refill control, and pre-service communication.

The project translates a culinary and hospitality operations problem into a data science and machine learning project.

### 2. Problem Statement

Hotel buffet kitchens often prepare and refill food based on experience rather than structured consumption data. This may result in overproduction, unnecessary leftovers, and higher food costs.

The key question of this project is:

How can data science help predict high waste risk and support better buffet production and refill decisions?

### 3. Dataset

The project uses a synthetic operational dataset based on a realistic leftover monitoring structure.

The dataset includes 500 buffet operation records with fields such as:

- meal period
- dish name
- dish category
- kitchen section
- estimated guests
- actual guests
- event type
- occupancy rate
- prepared quantity
- leftover quantity
- leftover ratio
- service time remaining
- refill count
- waste level
- recommended action

### 4. Methods

The project applies:

- Python for data processing
- pandas for data analysis
- matplotlib and Plotly for visualisation
- scikit-learn for machine learning
- Random Forest classification for high waste risk prediction
- Streamlit for dashboard deployment

### 5. Key Findings

Cold Dishes and Cold / Prep showed the highest average leftover ratios, suggesting that cold dishes, side toppings, and pre-prepared items may require closer monitoring and smaller batch preparation.

Normal buffet service showed a higher average leftover ratio than banquet, group tour, and wedding events. This suggests that normal service may require stronger forecasting and leftover monitoring because guest demand is less predictable.

### 6. Machine Learning Model

The final model is a binary classification model that predicts whether a buffet item is a high waste risk.

Model performance:

- Accuracy: 0.6800
- Precision: 0.5122
- Recall: 0.6364
- F1-score: 0.5676
- ROC-AUC: 0.7363

In this operational context, recall is important because the kitchen needs to identify as many high waste risk cases as possible.

### 7. Dashboard Output

The Streamlit dashboard includes:

1. Dataset overview
2. Waste level distribution
3. Top dishes by average leftover ratio
4. Waste analysis by kitchen section, meal period, and event type
5. High waste risk prediction form
6. Operational recommendation module

Example result:

A dinner cold dish in the Cold Dishes section under normal service, rainy weather, low occupancy, final 15 minutes of service, and 3 refills was predicted as High Waste Risk with a probability of 80.92%.

### 8. Operational Value

This project demonstrates how data science can support hospitality operations by:

- converting buffet operations into structured data
- identifying high-risk dishes and sections
- supporting production quantity adjustment
- improving refill decision-making
- reducing avoidable food waste
- connecting culinary management knowledge with data science methods

### 9. Relevance to Graduate Study

This project supports my transition from Culinary Management to Data Science and Artificial Intelligence.

It reflects my interest in applying data science and AI to hospitality operations, foodservice analytics, menu intelligence, demand forecasting, and sustainable kitchen management.

