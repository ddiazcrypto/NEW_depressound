def calculation(jitter, shimmer, f1, f2, hnr, gender,quantity_depression_words):
    # gender 1 male, 2 female
    calculated_result = 0
    if gender == 1:
        calculated_result = calculate_male(jitter, shimmer, f1, f2, hnr)
    else:
        calculated_result =  calculate_female(jitter, shimmer, f1, f2, hnr)
    return result_parameters(calculated_result), calculated_result

def calculate_male(jitter, shimmer, f1, f2, hnr):
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

def calculate_female(jitter, shimmer, f1, f2, hnr):
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


def result_parameters(calculation):
    if (calculation > 0 and calculation <= 1.5):
        return 'Sin depresión o Depresion minima', 1
    elif (calculation >= 2 and calculation <= 3.5):
        return 'Depresion leve', 2
    elif (calculation >= 5 and calculation <= 7):
        return 'Depresion moderada', 3
    elif (calculation >= 7.5 and calculation <= 8.5):
        return 'Depresion moderadamente severa', 4
    elif (calculation > 8.5 and calculation <= 10):
        return 'Depresion muy severa', 5

def result_words(words_calculation):
    if (words_calculation > 0 and words_calculation <= 17):
        return 'Sin depresión o Depresion minima', 1
    elif (words_calculation >= 18 and words_calculation <= 22):
        return 'Depresion leve', 2
    elif (words_calculation >= 23 and words_calculation <= 25):
        return 'Depresion moderada', 3
    elif (words_calculation >= 25 and words_calculation <= 27):
        return 'Depresion moderadamente severa', 4
    elif (words_calculation > 28 and words_calculation <= 30):
        return 'Depresion muy severa', 5

def diagnosis(score_parameters, score_words, diagnosis):
    return 'Se obtuvo un puntaje de ${score_parameters} en la evaluación de este audio por parametros de voz. En cuanto a la evaluación por palabras dichas se obtuvo el puntaje de ${score_words}. Lo cual da el siguiente diagnostico: ${diagnosis}'