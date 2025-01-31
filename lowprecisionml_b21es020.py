# -*- coding: utf-8 -*-
"""LowPrecisionML_B21ES020.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gaqzmqw10ftNpyJ7wtehpsP7qbzdS-24
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Task 1: Quantization of Input Data
def quantize_data(data, bits):
    levels = 2 ** bits
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    quantized_data = np.round(((data - min_val) / (max_val - min_val)) * (levels - 1)) * (max_val - min_val) / (levels - 1) + min_val
    return quantized_data

# Load dataset (using Iris as an example)
from sklearn.datasets import load_iris
data = load_iris()
X, y = data.data, data.target

# Task 2: Training and Evaluation with Quantized Data (Cross-Validation)
def evaluate_model(model, X, y):
    skf = StratifiedKFold(n_splits=5)
    scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
    return scores.mean(), scores.std()

# Models to evaluate
models = {
    'Decision Tree': DecisionTreeClassifier(),
    'k-NN': KNeighborsClassifier(),
    'SVM': SVC()
}

# Store results for different precision levels
results = {
    'Full-precision': {},
    '8-bit': {},
    '4-bit': {},
    '2-bit': {}
}

# Full-precision model evaluation
for model_name, model in models.items():
    mean_accuracy, std_accuracy = evaluate_model(model, X, y)
    results['Full-precision'][model_name] = (mean_accuracy, std_accuracy)

# Quantized models evaluation
for bits in [8, 4, 2]:
    quantized_X = quantize_data(X, bits)
    for model_name, model in models.items():
        mean_accuracy, std_accuracy = evaluate_model(model, quantized_X, y)
        results[f'{bits}-bit'][model_name] = (mean_accuracy, std_accuracy)

# Task 3: Comparison with Full-Precision Models
print("Performance Comparison (Mean Accuracy ± Std):")
for precision, precision_results in results.items():
    print(f"\n{precision}:")
    for model_name, (mean_accuracy, std_accuracy) in precision_results.items():
        print(f"{model_name}: {mean_accuracy:.4f} ± {std_accuracy:.4f}")

# Task 4: Impact Analysis - Plotting results
plt.figure(figsize=(10, 6))
for model_name in models.keys():
    accuracies = [results[precision][model_name][0] for precision in ['Full-precision', '8-bit', '4-bit', '2-bit']]
    plt.plot(['Full-precision', '8-bit', '4-bit', '2-bit'], accuracies, marker='o', label=model_name)

plt.xlabel('Precision Level (bits)')
plt.ylabel('Mean Accuracy')
plt.title('Model Accuracy vs. Precision Level')
plt.legend()
plt.grid()
plt.show()

# Task 5: Logistic Regression with Quantized Gradient Descent
log_reg_full = LogisticRegression(max_iter=1000)
log_reg_full.fit(X, y)
log_reg_full_pred = log_reg_full.predict(X)
accuracy_full = accuracy_score(y, log_reg_full_pred)

log_reg_quantized = QuantizedLogisticRegression(bits=4)
log_reg_quantized.fit(X, y)
log_reg_quant_pred = log_reg_quantized.predict(X)
accuracy_quant = accuracy_score(y, log_reg_quant_pred)

print(f"\nFull-precision Logistic Regression accuracy: {accuracy_full:.4f}")
print(f"Quantized gradient Logistic Regression accuracy: {accuracy_quant:.4f}")

