# 🧼 The Power of Handwashing: Dr. Semmelweis’ Discovery

## 📖 Introduction

In the mid-1800s, Dr. Ignaz Semmelweis worked at the Vienna General Hospital and made a groundbreaking observation: 
**handwashing drastically reduced deaths from childbed fever** among women giving birth. This project analyzes historical
data to investigate the impact of handwashing on maternal death rates using Python and data visualization tools.



---

## 🗂️ Dataset

The project uses two CSV files:

- `monthly_deaths.csv`: Monthly number of births and deaths.
- `annual_deaths_by_clinic.csv`: Yearly data split by clinic (Clinic 1 and Clinic 2).

---

## 🧪 What the Script Does

This Python script performs the following steps:

### 1. 📊 Data Loading & Exploration

- Loads the datasets using `pandas`.
- Checks for missing or duplicate values.
- Displays basic statistics and column info.

### 2. 📉 Visual Analysis

- Plots **total births vs. deaths over time**.
- Compares **death rates between the two clinics**.
- Highlights the **introduction of handwashing in 1847**.

### 3. 📈 Time Series Analysis

- Calculates a **6-month rolling average** death rate.
- Creates line plots to show trends before and after handwashing.

### 4. 📦 Statistical Summary

- Computes the **percentage of deaths** before and after handwashing.
- Shows how **handwashing reduced maternal mortality**.
- Uses **box plots, histograms, and KDE plots** to visualize distributions.

### 5. 📐 Statistical Testing

- Performs a **t-test** to evaluate if the reduction in deaths was statistically significant.

---

## 📌 Key Findings

- The death rate dropped **significantly** after handwashing was introduced.
- The **chance of dying in childbirth** was over 10 times lower after handwashing became mandatory.

---

## 🛠️ Libraries Used

- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `plotly.express`
- `scipy.stats`

---

## 📷 Sample Visualizations

- 📈 Yearly deaths by clinic
- 📉 Death rate trend before and after handwashing
- 📦 Box plots comparing before/after
- 📊 KDE plots for smooth death rate distribution

---

## 🚀 How to Run

1. Clone the repository
2. Install required libraries
3. Run the script in your Python environment or Jupyter notebook

```bash
pip install pandas numpy matplotlib seaborn plotly scipy
