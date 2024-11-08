import numpy as np
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

finaldiseases = pd.read_csv('/content/drive/MyDrive/finaldiseases.csv')
finaldiseases.head()

def generate_symptom_list():
    # Step 1: Create an empty list of length 377
    symptoms_list = [0] * 377

    # Step 2: Set first 30 values to 1 in 60% of them
    num_ones_30 = int(0.01 * 200)
    ones_indices_30 = np.random.choice(range(30), num_ones_30, replace=False)
    for idx in ones_indices_30:
        symptoms_list[idx] = 1

    # Step 3: Set any 8 values between index 10 and 20 to 1
    ones_indices_10_20 = np.random.choice(range(50, 200), 15, replace=False)
    for idx in ones_indices_10_20:
        symptoms_list[idx] = 1

    return symptoms_list

# Generate multiple lists, e.g., 5 lists for demonstration
symptom_lists = [generate_symptom_list() for _ in range(5)]

# Display the generated lists
for i, lst in enumerate(symptom_lists, 1):
    print(f"Symptom List {i}: {lst[:40]}")  # Displaying only the first 40 values for brevity


import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder  # You may already have this if you trained the model
import pickle

# Assuming you already have your lists
prediction_list = []
prediction_list_prob = []
extra_prediction_list = []
extra_prediction_list_prob = []

# 1. Load your model
model = tf.keras.models.load_model('/content/drive/MyDrive/Model_2_better.keras')

# 2. Load or define the label encoder (if not already loaded)
with open('/content/drive/MyDrive/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# 3. Prepare your input symptoms array (ensure it's a list of 377 values: 0s and 1s)
# Example input (replace with your actual symptom data list of 377 binary values):
input_symptoms_list = symptom_lists[0]  # Length should be 377 (with 0 and 1 values)

# Convert the input list to a numpy array and reshape it for prediction
input_data = np.array(input_symptoms_list).reshape(1, -1)  # Shape should be (1, 377)

# 4. Make a prediction using the model
predicted_probabilities = model.predict(input_data)

# 5. Get the indices of the top predictions
sorted_indices = np.argsort(predicted_probabilities[0])[::-1]  # Sort indices in descending order

# 6. Map the predicted class indices to the disease labels
predicted_diseases = label_encoder.inverse_transform(sorted_indices)

# 7. Check the maximum probability
max_prob = predicted_probabilities[0][sorted_indices[0]]

# 8. Handle the case where max probability is less than 0.5
if max_prob < 0.5:
    print("Model is not sure, but here are the most probable diseases:")
    top_predictions = []
    first_prob = predicted_probabilities[0][sorted_indices[0]]
    top_predictions.append((predicted_diseases[0], first_prob))

    # Add the next two predictions if their probability is at least 0.2 lower than the first
    for i in range(1, min(3, len(sorted_indices))):
        next_prob = predicted_probabilities[0][sorted_indices[i]]
        if first_prob - next_prob <= 0.2:
            top_predictions.append((predicted_diseases[i], next_prob))

    # Print the top 3 predictions
    for idx, (disease, prob) in enumerate(top_predictions):
        print(f"Top {idx + 1} Predicted Disease: \"{disease}\" with Probability: {prob:.4f}")
        prediction_list.append(disease)
        prediction_list_prob.append(prob)

    # Add the extra prediction (just the next one)
    extra_prediction = predicted_diseases[len(top_predictions)]  # Get the next best prediction
    extra_prob = predicted_probabilities[0][sorted_indices[len(top_predictions)]]
    print(f"Extra Prediction: \"{extra_prediction}\" with Probability: {extra_prob:.4f}")
    extra_prediction_list.append(extra_prediction)
    extra_prediction_list_prob.append(extra_prob)

# 9. If max probability is 0.5 or greater, follow the original logic
else:
    # Initialize variables to track the top predictions
    top_predictions = []
    first_prob = predicted_probabilities[0][sorted_indices[0]]

    # Add the first prediction
    top_predictions.append((predicted_diseases[0], first_prob))

    # Loop through the next predictions and add them if their probability is at least 0.2 lower than the first
    for i in range(1, len(sorted_indices)):
        next_prob = predicted_probabilities[0][sorted_indices[i]]
        if first_prob - next_prob <= 0.2:
            top_predictions.append((predicted_diseases[i], next_prob))
        else:
            break  # If the next prediction is more than 0.2 lower, stop adding predictions

    # Print the top predictions
    for idx, (disease, prob) in enumerate(top_predictions):
        print(f"Top {idx + 1} Predicted Disease: \"{disease}\" with Probability: {prob:.4f}")
        prediction_list.append(disease)
        prediction_list_prob.append(prob)

    # Add the extra prediction (just the next one)
    extra_prediction = predicted_diseases[len(top_predictions)]  # Get the next best prediction
    extra_prob = predicted_probabilities[0][sorted_indices[len(top_predictions)]]
    print(f"Extra Prediction: \"{extra_prediction}\" with Probability: {extra_prob:.4f}")

    # Append to both lists (extra prediction and its probability)
    extra_prediction_list.append(extra_prediction)
    extra_prediction_list_prob.append(extra_prob)

# Final output
print(f"Top Prediction list : {prediction_list}")
print(f"Extra Prediction list : {extra_prediction_list}")

import ast

def get_unique_medicines(prediction_list, finaldiseases):
    results = []
    for disease in prediction_list:
        drug_info = finaldiseases[finaldiseases['disease'] == disease]['drug'].values
        if len(drug_info) > 0:
            actual_drug_list = ast.literal_eval(drug_info[0])
            if isinstance(actual_drug_list, list):
                unique_drugs = list(set(actual_drug_list))
                results.append((disease, unique_drugs))
    return results

result = get_unique_medicines(prediction_list, finaldiseases)
result_extra = get_unique_medicines(extra_prediction_list, finaldiseases)

def get_first_5_medicines(result_list):
    return [(disease, medicines[:5]) for disease, medicines in result_list]
result_frst5 = get_first_5_medicines(result)
result_extrafrst5 = get_first_5_medicines(result_extra)

for disease, medicines in result_frst5:
    print(f"Disease: {disease}, First 5 Medicines: {medicines}")
for disease, medicines in result_extrafrst5:
    print(f"Disease: {disease}, First 5 Medicines: {medicines}")


print(f"Top Prediction list : {prediction_list}")
print(prediction_list_prob)
print(f"Extra Prediction list : {extra_prediction_list}")
print(extra_prediction_list_prob)
for disease, medicines in result_frst5:
    print(f"Disease: {disease}, First 5 Medicines: {medicines}")
for disease, medicines in result_extrafrst5:
    print(f"Disease: {disease}, First 5 Medicines: {medicines}")

print(result_frst5)

#current_medication = [] input list, using dropdown or NLP

all_medicines = []
for disease, medicines in result_frst5 + result_extrafrst5:
    all_medicines.extend(medicines)  # Add all medicines for each disease to the list

# Remove duplicates by converting the list to a set and back to a list
all_medicines = list(set(all_medicines))

# Print the result
print(all_medicines)

#First for individual medicine side effects
singledrugeffect = pd.read_csv('/content/drive/MyDrive/singledrugsideeffect.csv')
subsandse = pd.read_csv('/content/drive/MyDrive/Substitute and side effects.csv')
subsandse.head()

subsandse.head()

# Function to get side effects for medicines in all_medicines list
def get_side_effects_for_medicines(all_medicines, drug_df):
    medicine_side_effects = {}

    for medicine in all_medicines:
        # First check if the medicine is in the 'drug_name' column
        row = drug_df[drug_df['drug_name'].str.lower() == medicine.lower()]

        if not row.empty:
            # If found, get the side effects from the 'side_effects' column
            medicine_side_effects[medicine] = row.iloc[0]['side_effects']
        else:
            # If not found in 'drug_name', check the 'generic_name' column
            row = drug_df[drug_df['generic_name'].str.lower() == medicine.lower()]
            if not row.empty:
                # If found in 'generic_name', get the side effects
                medicine_side_effects[medicine] = row.iloc[0]['side_effects']

    return medicine_side_effects

# Get the side effects for all medicines
side_effects_dict = get_side_effects_for_medicines(all_medicines, singledrugeffect)

# Print the result
print(side_effects_dict)
num_pairs = len(side_effects_dict)
print(num_pairs)
medwse = list(side_effects_dict.keys())
print(medwse)

druginteraction = pd.read_csv('/content/drive/MyDrive/druginteractionsfinal.csv')


import itertools

# Function to get interactions for all medicine pairs
def get_interactions_for_pairs(all_medicines, interaction_df):
    interaction_dict = {}

    # Generate all unique pairs of medicines
    for drug1, drug2 in itertools.combinations(all_medicines, 2):
        # Check for both (Drug_A, Drug_B) and (Drug_B, Drug_A)
        pair1 = interaction_df[(interaction_df['Drug_A'].str.lower() == drug1.lower()) & (interaction_df['Drug_B'].str.lower() == drug2.lower())]
        pair2 = interaction_df[(interaction_df['Drug_A'].str.lower() == drug2.lower()) & (interaction_df['Drug_B'].str.lower() == drug1.lower())]

        # If an interaction is found for either pair, add to the dictionary
        if not pair1.empty:
            interaction_dict[(drug1, drug2)] = {
                'Interaction': pair1.iloc[0]['Interaction'],
                'Risk_Level': pair1.iloc[0]['Risk_Level']
            }
        elif not pair2.empty:
            interaction_dict[(drug2, drug1)] = {
                'Interaction': pair2.iloc[0]['Interaction'],
                'Risk_Level': pair2.iloc[0]['Risk_Level']
            }

    return interaction_dict

# Get the interactions for all pairs of medicines
interaction_results = get_interactions_for_pairs(all_medicines, druginteraction)

# Print the results
#for pair, details in interaction_results.items():
#    print(f"Pair: {pair}")
#    print(f"  Interaction: {details['Interaction']}")
#    print(f"  Risk Level: {details['Risk_Level']}")
#    print()
print(interaction_results)

