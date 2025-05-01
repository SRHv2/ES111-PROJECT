#--------------------------------------------ES111 SPRING 2025 PROJECT-------------------------------------------#
#Group Members' Reg #s:
# 2024621
# 2024590
# 2024106 

import numpy as np
import matplotlib.pyplot as plt
#-------------READ THE FILE---------------
def find_word_array_and_length(parafile):
    """Reads ALL words from a file, regardless of lines."""
    with open(parafile, 'r') as file:
        text = file.read()  
        words = text.split()  
    
    word_array = np.array(words)
    word_lengths = np.char.str_len(word_array)
    return word_array, word_lengths

# -------------FIND MEAN AND VARIANCE FROM THE FILE DATASET---------------
file_path = 'dataset_of_words'
word_array, word_lengths = find_word_array_and_length(file_path)

mean=np.mean(word_lengths)
variance=np.var(word_lengths)
print(f"Mean: {mean:.3f}")
print(f"Variance: {variance:.3f}")


#--------------CATEGORIZE DATA----------------------
w2, w3, w4, w5, w6, w7, w8, w9, w10 = [], [], [], [], [], [], [], [], []
w11, w12, w13, w14, w15, w16, w17, w18, w19, w20 = [], [], [], [], [], [], [], [], [], []

for value in word_lengths:
    if 2 <= value <= 20:  
        target_array = globals()[f'w{value}']
        target_array.append(value)
for i in range(2, 21):
    globals()[f'w{i}len'] = len(globals()[f'w{i}'])


#-------------------MAKE GRAPHS-----------------------------------------------
categories = [str(i) for i in range(2, 21)]  
values = [globals()[f'w{i}len'] for i in range(2, 21)]
group_ranges = [(2,5), (6,9), (10,13), (14,17), (18,20)]
group_labels = ["2-5", "6-9", "10-13", "14-17", "18-20"]
grouped_values = [sum(values[start-2:end-1]) for start,end in group_ranges]
plt.figure(figsize=(18, 6))
plt.subplot(1, 2, 1)
bars = plt.bar(categories, values)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}', ha='center', va='bottom')
plt.title('Word Length Distribution Histogram')
plt.xlabel('Word Lengths')
plt.ylabel('Frequency')
plt.subplot(1, 2, 2)
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
explode = (0.05, 0.05, 0.05, 0.05, 0.1) 
wedges, texts, autotexts = plt.pie(
    grouped_values,
    explode=explode,
    labels=group_labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    shadow=True,
    textprops={'fontsize': 12}
)
plt.setp(autotexts, size=12, weight="bold")  
plt.title('Word Length Distribution (Grouped)', fontsize=14)
plt.tight_layout(pad=3.0)
plt.show()

#-----------------------GENERATE FREQUENCY TABLE, FIND ITS MEAN AND VARIANCE------------

unique_lengths, counts = np.unique(word_lengths, return_counts=True)

print("\nFrequency Distribution Table:")
print("-"*40)
print("Word Length   Frequency")
print("-" * 40)
for length, count in zip(unique_lengths, counts):
    print(f"{length}\t\t{count} ")
sum=0
for length, count in zip(unique_lengths, counts):
    sum+=length*count
fqtable_mean=sum/counts.sum()
sum=0
for i in range(len(word_lengths)):
    sum +=(word_lengths[i]-fqtable_mean)**2
fqtable_variance = sum/ (counts.sum()-1)
print(f"\nMean from the frequency table: {fqtable_mean:.3f}")
print(f"Variance from the frequency table: {fqtable_variance:.3f}")

#-----------------FIND CONFIDENCE AND TOLERANCE INTERVAL OF 80% OF THE DATASET, COMPARE WITH REMAINING 20%----------------

train_data = []
test_data = []
for i in range(len(word_lengths)):
    if i<800:
        train_data.append(word_lengths[i])
    else:
        test_data.append(word_lengths[i])
train_mean=np.mean(train_data)
train_variance=np.var(train_data)                                  #standard deviation is square root of variance
train_confidence_lower = train_mean - 1.96*((train_variance/len(train_data))**.5 ) #z value at 95% interval is 1.96
train_confidence_upper = train_mean + 1.96*((train_variance/len(train_data))**.5 ) #c1 and c2 represents two 
                                                                 #ends of the interval
print(f"\nConfidence Interval for 80% of the dataset:'['{train_confidence_upper:.3f} , {train_confidence_lower:.3f} ']' ")
tolerance_lower = train_mean - 1.96*(train_variance**.5) 
tolerance_upper = train_mean + 1.96*(train_variance**.5)
print(f"\nTolerance Interval: '['{tolerance_upper} , {tolerance_lower}']'")
test_mean=np.mean(test_data)
test_inside_confidence = train_confidence_lower<= test_mean and test_mean<=train_confidence_upper
test_inside_tolerance = np.sum((test_data>=tolerance_lower) & (test_data<=tolerance_upper))/len(test_data)
print("\nValidation Results:")
print(f"Test mean ({test_mean:.3f}) is {'WITHIN' if test_inside_confidence else 'OUTSIDE'} the CI")
print(f"{test_inside_tolerance*100:.1f}% of test data falls within the tolerance interval")


