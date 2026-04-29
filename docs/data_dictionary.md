# Cleaned Dataset Data Dictionary

This document explains the columns available in the `data/processed/cleaned_data.csv` dataset, what they represent, and the type of values they contain.

| Column Name | Description | Value Type / Examples |
| :--- | :--- | :--- |
| **student_id** | Unique identifier for each student | Integer (e.g., 1, 2, 3...) |
| **country** | The country where the student resides | String (e.g., USA, India, UK) |
| **development_level** | Economic development level of the country | String (e.g., Developed, Developing) |
| **poverty_rate_percent** | The poverty rate of the student's region or country | Float (Percentage, e.g., 12.32) |
| **internet_infrastructure_index** | Score representing the quality of internet infrastructure | Float (e.g., 66.87, 90.50) |
| **average_internet_speed_mbps** | Average internet speed available to the student | Float (Mbps, e.g., 45.63, 188.19) |
| **age** | Age of the student | Integer (e.g., 15, 18, 21) |
| **gender** | Gender of the student | String (`Male`, `Female`, `Other`) |
| **urban_rural** | The type of living environment | String (`Urban`, `Rural`) |
| **family_income_level** | Family's income tier | String (`High`, `Middle`, `Low`) |
| **device_access** | Type of device(s) primarily used | String (`Both`, `Smartphone`, `Laptop`, `Shared Device`) |
| **internet_access_hours** | Total hours of internet access per day | Float (Hours, e.g., 6.25) |
| **education_level** | Current educational stage | String (`School`, `Graduate`, `Diploma`, `Dropout`, `PhD`) |
| **field_of_study** | Area of academic study | String (`Law`, `Social Sciences`, `Business`, `Medicine`, `Arts`) |
| **academic_motivation** | Score representing the student's motivation towards academics | Float (e.g., 3.66, 8.00) |
| **online_learning_hours** | Hours spent on online learning platforms per day | Float (Hours, e.g., 5.45) |
| **social_media_hours** | Hours spent on social media per day | Float (Hours, e.g., 4.75) |
| **sessions_per_day** | Number of distinct digital sessions per day | Float (e.g., 13.97) |
| **average_session_length_minutes** | Average length of each digital session | Float (Minutes, e.g., 56.63) |
| **late_night_usage** | Frequency of device usage late at night | String (`Sometimes`, `Often`, `Always`, `Never`) |
| **education_content_hours** | Hours spent consuming educational content per day | Float (Hours, e.g., 0.94) |
| **short_video_hours** | Hours spent watching short-form videos (e.g., TikTok, Reels) | Float (Hours, e.g., 2.80) |
| **entertainment_content_hours** | Hours spent on general entertainment content per day | Float (Hours, e.g., 1.94) |
| **news_content_hours** | Hours spent consuming news media per day | Float (Hours, e.g., 0.55) |
| **likes_given_per_day** | Average number of likes given on social platforms | Float (e.g., 132.14) |
| **comments_written_per_day** | Average number of comments written per day | Float (e.g., 16.08) |
| **posts_created_per_week** | Average number of posts created per week | Float (e.g., 4.34) |
| **late_night_score** | Numerical severity score of late-night usage | Integer (e.g., 0, 1, 2, 3) |
| **brain_rot_index** | Calculated index indicating consumption of passive, low-quality content | Float (e.g., 10.99, 29.85) |
| **brain_rot_level** | Categorical tier based on the brain rot index | String (`Low`, `Medium`, `High`) |
| **attention_span_minutes** | Measured or self-reported attention span | Float (Minutes, e.g., 47.74, 60.00) |
| **study_hours_per_week** | Total hours spent studying per week | Float (Hours, e.g., 26.25) |
| **class_attendance_rate** | Percentage of scheduled classes attended | Float (Percentage, e.g., 90.68) |
| **productivity_score** | Score representing overall daily productivity | Float (e.g., 5.76, 10.00) |
| **sleep_hours** | Average hours of sleep per night | Float (Hours, e.g., 5.85) |
| **stress_level** | Calculated or self-reported stress level | Float (e.g., 3.38, 6.19) |
| **anxiety_score** | Score representing the severity of anxiety symptoms | Float (e.g., 4.16, 7.48) |
| **depression_score** | Score representing the severity of depressive symptoms | Float (e.g., 2.42, 8.43) |
| **ads_viewed_per_day** | Number of digital advertisements viewed per day | Float (e.g., 139.74) |
| **ads_clicked_per_week** | Number of digital advertisements clicked per week | Float (e.g., 13.72) |
| **impulse_purchase_score** | Score indicating the tendency to make impulse digital purchases | Float (e.g., 5.39, 7.78) |
| **digital_spending_per_month** | Amount of money spent on digital goods/services | Float (Currency value, e.g., 106.59) |
| **cyberbullying_exposure** | Indicates if the student has been exposed to cyberbullying | Integer (`1` = Yes, `0` = No) |
| **adult_content_exposure** | Indicates if the student has been exposed to adult content | Integer (`1` = Yes, `0` = No) |
| **digital_addiction_score** | Score representing the severity of digital addiction | Float (e.g., 8.29, 20.24) |
| **wellbeing_index** | Overall index summarizing physical and mental wellbeing | Float (e.g., 49.71, 71.06) |
| **academic_risk_score** | Engineered metric estimating the risk of academic failure | Float (e.g., 15.35, 38.87) |
| **financial_risk_score** | Engineered metric estimating financial risk due to online behavior | Float (e.g., 36.33, 53.90) |
