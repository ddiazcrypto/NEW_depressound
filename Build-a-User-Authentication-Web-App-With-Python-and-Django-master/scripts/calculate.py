def calculation(jitter, shimmer, f1, f2, hnr, gender,quantity_depression_words):
    # gender 1 male, 2 female
    calculated_result_parameters = 0
    if gender == 1:
        calculated_result_parameters = calculate_male(jitter, shimmer, f1, f2, hnr)
    else:
        calculated_result_parameters =  calculate_female(jitter, shimmer, f1, f2, hnr)
    result_parameters_var = result_parameters(calculated_result_parameters)
    result_words_var = result_words(quantity_depression_words)
    final_result = (result_parameters_var*2+result_words_var)/2
    diagnosis_text = final_diagnosis_text(round(final_result))
    result_parameters_var_diagnosis = final_diagnosis_text(round(result_parameters_var))
    result_words_var_diagnosis = final_diagnosis_text(round(result_words_var))
    return diagnosis_text, diagnosis(calculated_result_parameters, quantity_depression_words, diagnosis_text, result_parameters_var_diagnosis, result_words_var_diagnosis), calculated_result_parameters, quantity_depression_words, result_parameters_var, result_words_var, round(final_result)

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
    if (calculation >= 0 and calculation <= 1.5):
        return 1
    elif (calculation >= 2 and calculation <= 3.5):
        return 2
    elif (calculation >= 4.5 and calculation <= 7):
        return 3
    elif (calculation >= 7.5 and calculation <= 8.5):
        return 4
    elif (calculation > 8.5 and calculation <= 10):
        return 5
    return 0    

def result_words(words_calculation):
    if (words_calculation > 0 and words_calculation <= 17):
        return 1
    elif (words_calculation >= 18 and words_calculation <= 22):
        return 2
    elif (words_calculation >= 23 and words_calculation <= 25):
        return 3
    elif (words_calculation > 25 and words_calculation <= 27):
        return 4
    elif (words_calculation > 28 and words_calculation <= 30):
        return 5
    return 0    

def final_diagnosis_text(scale):
    if (scale == 1):
        return 'Sin depresión o Depresion minima'
    elif (scale == 2):
        return 'Depresion leve'
    elif (scale == 3):
        return 'Depresion moderada'
    elif (scale == 4):
        return 'Depresion moderadamente severa'
    elif (scale == 5):
        return 'Depresion muy severa'
    return 'No se puedo obtener análisis, vuelva a intentar'    

def diagnosis(score_parameters, score_words, diagnosis, result_parameters_var_diagnosis, result_words_var_diagnosis):
    return f'Se obtuvo un puntaje de {score_parameters} en la evaluación de este audio por parametros de voz, lo cual significa que en esta etapa el paciente tiene el siguiente diagnostico: {result_parameters_var_diagnosis}. En cuanto a la evaluación por palabras dichas se obtuvo el puntaje de {score_words}, lo cual se traduce a que en esta etapa el paciente tiene el siguiente resultado: {result_words_var_diagnosis}, haciendo un analisis de ambos, resulta el siguiente diagnostico final: {diagnosis}'
