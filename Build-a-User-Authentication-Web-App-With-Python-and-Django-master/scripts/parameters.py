import speech_recognition as sr
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
import csv

import glob
import numpy as np
import pandas as pd
import parselmouth 
import statistics
from parselmouth.praat import call
import sys
mysp=__import__("my-voice-analysis")

# Calculations

def evaluate_pc(pc):
    if pc <=10:
        return 0
    elif pc >= 11 and pc <= 20:
        return 3    
    elif pc >= 21 and pc <= 25:
        return 5
    elif pc > 25:
        return 10

def evaluate_p1(p1):
    if p1 <= 10:
        return 0
    elif p1 >= 11 and p1 <= 20:
        return 5
    elif p1 > 20:
        return 10

def evaluate_p2(p2):
    if p2 <= 5:
        return 0
    elif p2 > 5 and p2 <= 10:
        return 1    
    elif p2 > 10:
        return 5

def evaluate_p12(p12):
    if p12 <= 30:
        return 5
    else:
        return 0                          

def find_depression_words(data):
    if data is None:
        raise Exception("Empty Data")
    
    words = data.split()
    new_text = ""
    word_count = 0
    word_total_count_pt = 0
    for word in words:
        new_text += word + " "
        word_count += 1
        if word_count == 10:
            new_text += ","
            word_count = 0
        word_total_count_pt += 1    

    words_splitted = new_text.split(',')
    count_depression_words_pc = 0
    count_depression_words_p1 = 0
    count_depression_words_p2 = 0
    validator_pc = Palabrota(countries=[Country.COLOMBIA]) # depression words
    validator_p1 = Palabrota(countries=[Country.VENEZUELA]) # 1st person pronouns
    validator_p2 = Palabrota(countries=[Country.MEXICO]) #2nd and 3rd person pronouns

    for texto in words_splitted:
        print('texto ', texto)
        if isinstance(texto, str):
            is_depression_word_pc = validator_pc.contains_palabrota(texto)
            is_depression_word_p1 = validator_p1.contains_palabrota(texto)
            is_depression_word_p2 = validator_p2.contains_palabrota(texto)

            if is_depression_word_pc:
                count_depression_words_pc += 1
            if is_depression_word_p1:
                count_depression_words_p1 += 1    
            if is_depression_word_p2:
                count_depression_words_p2 += 1    
    
    pc_percentage = (count_depression_words_pc * 100)/word_total_count_pt
    p1_percentage = (count_depression_words_p1 * 100)/word_total_count_pt
    p2_percentage = (count_depression_words_p2 * 100)/word_total_count_pt    
    p12_percentage = 0
    if p1_percentage == 0: p12_percentage = 0
    else: p12_percentage = (p2_percentage * 100)/p1_percentage

    print('pc_percentage ', pc_percentage)
    print('p1_percentage ', p1_percentage)
    print('p2_percentage ', p2_percentage)
    print('p12_percentage ', p12_percentage)

    total_evaluated_words = evaluate_pc(pc_percentage) + evaluate_p1(p1_percentage) + evaluate_p2(p2_percentage) + evaluate_p12(p12_percentage)
    print('total_evaluated_words ', total_evaluated_words)
    return total_evaluated_words

def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    duration = call(sound, "Get total duration") # duration
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    return duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer
# This function measures formants using Formant Position formula
def measureFormants(sound, wave_file, f0min,f0max):
    sound = parselmouth.Sound(sound) # read the sound
    pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []
    
    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)
    
    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
    f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
    f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']
    
    # calculate mean formants across pulses
    f1_mean = statistics.mean(f1_list)
    f2_mean = statistics.mean(f2_list)
    f3_mean = statistics.mean(f3_list)
    f4_mean = statistics.mean(f4_list)
    
    # calculate median formants across pulses, this is what is used in all subsequent calcualtions
    # you can use mean if you want, just edit the code in the boxes below to replace median with mean
    f1_median = statistics.median(f1_list)
    f2_median = statistics.median(f2_list)
    f3_median = statistics.median(f3_list)
    f4_median = statistics.median(f4_list)
    
    return f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median

def main_proccess(audio_file_name):
# create lists to put the results
    file_list = []
    duration_list = []
    mean_F0_list = []
    sd_F0_list = []
    hnr_list = []
    localJitter_list = []
    localabsoluteJitter_list = []
    rapJitter_list = []
    ppq5Jitter_list = []
    ddpJitter_list = []
    localShimmer_list = []
    localdbShimmer_list = []
    apq3Shimmer_list = []
    aqpq5Shimmer_list = []
    apq11Shimmer_list = []
    ddaShimmer_list = []
    f1_mean_list = []
    f2_mean_list = []
    f3_mean_list = []
    f4_mean_list = []
    f1_median_list = []
    f2_median_list = []
    f3_median_list = []
    f4_median_list = []

    wave2_file = glob.glob(audio_file_name+'.wav')

    sound = parselmouth.Sound(wave2_file[0])

# local shimmer, local jitter, f1_mean, f2_mean, hnr
    (duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, 
    localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer) = measurePitch(
        sound, 75, 300, "Hertz")

    (f1_mean, f2_mean, f3_mean, f4_mean, f1_median, f2_median, f3_median, f4_median) = measureFormants(
        sound, wave2_file[0], 75, 300)

    file_list.append(wave2_file[0]) # make an ID list
    duration_list.append(duration) # make duration list
    mean_F0_list.append(meanF0) # make a mean F0 list
    sd_F0_list.append(stdevF0) # make a sd F0 list
    hnr_list.append(hnr) #add HNR data
        
        # add raw jitter and shimmer measures
    localJitter_list.append(localJitter)
    localabsoluteJitter_list.append(localabsoluteJitter)
    rapJitter_list.append(rapJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    ddpJitter_list.append(ddpJitter)
    localShimmer_list.append(localShimmer)
    localdbShimmer_list.append(localdbShimmer)
    apq3Shimmer_list.append(apq3Shimmer)
    aqpq5Shimmer_list.append(aqpq5Shimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    ddaShimmer_list.append(ddaShimmer)
        
        # add the formant data
    f1_mean_list.append(f1_mean)
    f2_mean_list.append(f2_mean)
    f3_mean_list.append(f3_mean)
    f4_mean_list.append(f4_mean)
    f1_median_list.append(f1_median)
    f2_median_list.append(f2_median)
    f3_median_list.append(f3_median)
    f4_median_list.append(f4_median)
    r = sr.Recognizer()

    with sr.AudioFile(audio_file_name+'.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language="es-PE")
        except:
            print('Sorry.. run again...')

    total_evaluated_words = find_depression_words(text)

    return localShimmer, localJitter, f1_mean, f2_mean, hnr, total_evaluated_words

def male_female(audio_file_name):
    # example: audio is located in D:\audios\audio1.wav
    # so, p = audio1 ... don't add .wav
    # c = D:\audios ... don't add last \
    mysp=__import__("my-voice-analysis")
    original_stdout = sys.stdout
    gender_num = 4
    p=audio_file_name # Audio File title without .wav
    c=r"H:\Brigitte\8vo ciclo\Scripts\NEW_depressound\Build-a-User-Authentication-Web-App-With-Python-and-Django-master" # Path to the Audio_File directory (Python 3.7)

    with open('log.txt', 'w') as file:
        sys.stdout = file
        mysp.myspgend(p,c)
        sys.stdout = original_stdout
    with open('log.txt', 'r') as reader:
        printed_text = reader.read()
        str_file = printed_text.split()
        if 'male' in str_file:
            gender_num = 1
        elif 'female' in str_file:
            gender_num = 0
        print(printed_text)    
    return gender_num

def retrieve_all_results(audio_file_name):
    # formulas
    gender = male_female(audio_file_name)
    localShimmer, localJitter, f1_mean, f2_mean, hnr, total_evaluated_words = main_proccess(audio_file_name)
    return gender, localShimmer, localJitter, f1_mean, f2_mean, hnr, total_evaluated_words