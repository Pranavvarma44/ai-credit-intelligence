# AI Credit Intelligence

An end-to-end AI-powered credit risk prediction system that predicts the likelihood of loan default using machine learning.

The project compares **Random Forest** and **XGBoost**, uses **Stratified 5-Fold Cross-Validation** for model validation, performs threshold analysis for the imbalanced target, provides model explanations, and exposes the final model through a deployed web application.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Dataset](#dataset)
- [Features](#features)
- [Models](#models)
- [Model Validation](#model-validation)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Threshold Selection](#threshold-selection)
- [Model Evaluation](#model-evaluation)
- [NTC Case](#ntc-case)
- [What-If Analysis](#what-if-analysis)
- [Explainability](#explainability)
- [Application Flow](#application-flow)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Local Setup](#local-setup)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Database](#database)
- [Deployment](#deployment)
- [Testing](#testing)
- [Results](#results)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Demo](#demo)

---

# Project Overview

AI Credit Intelligence is a credit-risk prediction application designed to estimate whether a loan applicant is likely to default.

The system takes applicant information such as:

- Income
- Employment details
- Loan amount
- Loan tenure
- Existing debt
- Debt-to-income ratio
- Credit utilization
- Previous missed payments
- Repayment consistency
- Financial behavior
- New-to-credit status

and uses a trained machine learning model to generate a probability of default.

The project covers the complete machine learning and software-development pipeline:

```text
Data
  ↓
Preprocessing
  ↓
Model Training
  ↓
Cross-Validation
  ↓
Hyperparameter Tuning
  ↓
Model Evaluation
  ↓
Threshold Selection
  ↓
Model Explainability
  ↓
FastAPI Backend
  ↓
Frontend Application
  ↓
Deployment
