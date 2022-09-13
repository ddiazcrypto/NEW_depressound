import sys

def calculation(jitter, shimmer, f1, f2, hnr, gender,quantity_depression_words):
    # gender 1 male, 2 female
    calculated_result = 0
    if gender == 1:
        calculated_result = calculate_male(jitter, shimmer, f1, f2, hnr,quantity_depression_words)
    else:
        calculated_result =  calculate_female(jitter, shimmer, f1, f2, hnr,quantity_depression_words)
    return result(calculated_result), calculated_result    

def calculate_male(jitter, shimmer, f1, f2, hnr, quantity_depression_words):
    total_sum = 0
    if shimmer >= 0.1365 and shimmer <= 0.207:
        total_sum += 2.5
    if hnr >= 3.74 and hnr <= 7.9:
        total_sum += 2.5
    if jitter >= 0.035 and jitter <= 0.071:
        total_sum += 2
    if f1 >= 486.4 and f1 <= 520:
        total_sum += 1.5
    if f2 >= 1511.5 and f2 <= 1604:
        total_sum += 1.5
    return total_sum    



def calculate_female(jitter, shimmer, f1, f2, hnr,quantity_depression_words):
    total_sum = 0
    if shimmer >= 0.133 and shimmer <= 0.177:
        total_sum += 2.5
    if hnr >= 7.715 and hnr <= 8.384:
        total_sum += 2.5
    if jitter >= 0.0265 and jitter <= 0.0415:
        total_sum += 2
    if f1 >= 572 and f1 <= 632:
        total_sum += 1.5
    if f2 >= 1507.8 and f2 <= 1784:
        total_sum += 1.5
    return total_sum


def result(calculation):
    if (calculation > 0 and calculation <= 1.5):
        return 'Sin depresión o Depresion minima'
    elif (calculation >= 2 and calculation <= 3.5):
        return 'Depresion leve'
    elif (calculation >= 5 and calculation <= 7):
        return 'Depresion moderada'
    elif (calculation >= 7.5 and calculation <= 8.5):
        return 'Depresion moderadamente severa'
    elif (calculation > 8.5 and calculation <= 10):
        return 'Depresion muy severa'

def find_word_in_print():
    file = open('log.txt', 'w')
    print('This is a sample print male', file = file)
    file.close()
    file1 = open("log.txt","r+")
    str_file1 =  file1.read()
    str_file = str_file1.split()
    print(str_file)
    file1.close()

    if 'male' in str_file:
        print("success")        

def get_sys():
    original_stdout = sys.stdout 

    # Create or open an existing file in write mode
    with open('log.txt', 'w') as file:
        # Set the stdout to file object
        sys.stdout = file
        print('File Mode: Print text to a file. bru')
        
        # Set the stdout back to the original or default mode
        sys.stdout = original_stdout

    with open('log.txt', 'r') as reader:
        # Read & print the entire file
        printed_text = reader.read()
        print(printed_text)        