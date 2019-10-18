#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter
from math import log2, log
import numpy as np
import os


# In[2]:


#In case ocr output needs to be smoothed
def smooth_txt(txt):
    txt = txt.replace("\n"," ");
    txt = txt.replace("  "," ");
    return (txt)


# In[3]:


#Detect vowels and consonants, useful for further computations on probabilites
vowels = ["a","à","á","â","e","è","é","ê","i","ì","í","î","o","ò","ó","ô","u","ù","ú","û"]
conson = ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z","ñ","ç"]

def vow_con(txt):
    txt = txt.lower();
    for i in vowels+conson:
        if i in vowels:
            txt = txt.replace(i,"*")
        else:
            txt = txt.replace(i,"c")
    txt = txt.replace("*","v")
    return (txt)


# In[4]:


#Create modified versions of the texts
def lang_text(lang):
    file_name = "text/" + lang + ".txt"
    txt_lang_raw = open(file_name,"r",encoding="utf-8").read();
    txt_lang = smooth_txt(txt_lang_raw)
    txt_lang_par = txt_lang.split()
    txt_lang_vc = vow_con(txt_lang)
    return(txt_lang_raw, txt_lang, txt_lang_par, txt_lang_vc)


# In[5]:


#Load texts
langs = ["cat", "eng", "esp"]

txt_cat_raw, txt_cat, txt_cat_par, txt_cat_vc = lang_text("cat")
txt_eng_raw, txt_eng, txt_eng_par, txt_eng_vc = lang_text("eng")
txt_esp_raw, txt_esp, txt_esp_par, txt_esp_vc = lang_text("esp")


# In[6]:


#Average length of the languages words
langs_avg_len = [None] * len(langs)
langs_avg_len[0] = len(txt_cat.replace(' ',''))/len(txt_cat_par)
langs_avg_len[1] = len(txt_eng.replace(' ',''))/len(txt_eng_par)
langs_avg_len[2] = len(txt_esp.replace(' ',''))/len(txt_esp_par)


# In[7]:


#Most frequent words of the languages defined
def dictkey(dicti):
    keys = [None] * len(dicti)
    j = 0
    for i in dicti:
        keys[j] = i[1]
        j = j + 1
    return keys

def f_freq_words(langs, ranksize):
    freq_words = [None] * len(langs)
    p = dict(Counter(txt_cat_par)); p = [[p[x],x] for x in p]
    p.sort(reverse = True); freq_words[0] = dictkey(p[:ranksize])
    p = dict(Counter(txt_eng_par)); p = [[p[x],x] for x in p]
    p.sort(reverse = True); freq_words[1] = dictkey(p[:ranksize])
    p = dict(Counter(txt_esp_par)); p = [[p[x],x] for x in p]
    p.sort(reverse = True); freq_words[2] = dictkey(p[:ranksize])
    return freq_words

freq_words = f_freq_words(langs, 10)


# In[8]:


#Probs of a certain king of letter (vowel, consonant, space) wrt the following one
def prob(txt,par):
    t = txt+txt[:len(par)-1];
    return t.count(par)/len(txt)

def rel_prob(txt):
    return [[prob(txt,x+y) for y in ['v','c',' ']] for x in ['v','c',' ']]

def cond_prob(txt,y,z):
    w = y+z
    t = txt+txt[:len(w)-1];
    return t.count(w)/t.count(y)

def rel_cond_prob(txt):
    return [[cond_prob(txt,x,y) for y in ['v','c',' ']] for x in ['vv','vc','cv','cc',' v',' c']]


# In[9]:


rel_freqs = [None] * len(langs)
rel_freqs[0] = rel_prob(txt_cat_vc)
rel_freqs[1] = rel_prob(txt_eng_vc)
rel_freqs[2] = rel_prob(txt_esp_vc)


# In[10]:


rel_cond_freqs = [None] * len(langs)
rel_cond_freqs[0] = rel_cond_prob(txt_cat_vc)
rel_cond_freqs[1] = rel_cond_prob(txt_eng_vc)
rel_cond_freqs[2] = rel_cond_prob(txt_esp_vc)


# In[11]:


#Consecutive vowels and consonants
consec = [None] * len(langs)
consec[0] = [txt_cat_vc.count(3*'v'),txt_cat_vc.count(3*'c'),txt_cat_vc.count(4*'v'),txt_cat_vc.count(4*'c')]
consec[0] = list(map(lambda x: x/len(txt_cat_par), consec[0]))
consec[1] = [txt_eng_vc.count(3*'v'),txt_eng_vc.count(3*'c'),txt_eng_vc.count(4*'v'),txt_eng_vc.count(4*'c')]
consec[1] = list(map(lambda x: x/len(txt_eng_par), consec[1]))
consec[2] = [txt_esp_vc.count(3*'v'),txt_esp_vc.count(3*'c'),txt_esp_vc.count(4*'v'),txt_esp_vc.count(4*'c')]
consec[2] = list(map(lambda x: x/len(txt_esp_par), consec[2]))


# In[12]:


#Parameters of the input text
def input_z_create(file_name, lang):
    input_z = [None] * 5
    file_name = file_name + ".txt"
    txt_z_raw = open(file_name,"r",encoding="utf-8").read();
    txt_z = smooth_txt(txt_z_raw)
    txt_z_par = txt_z.split()
    txt_z_vc = vow_con(txt_z)
    input_z[0] = len(txt_z.replace(' ',''))/len(txt_z_par)
    p = dict(Counter(txt_z_par)); p = [[p[x],x] for x in p]; p.sort(reverse = True);
    input_z[1] = dictkey(p[:10])
    input_z[2] = rel_prob(txt_z_vc)
    input_z[3] = rel_cond_prob(txt_z_vc)
    input_z[4] = [txt_z_vc.count(3*'v'),txt_z_vc.count(3*'c'),txt_z_vc.count(4*'v'),txt_z_vc.count(4*'c')]
    input_z[4] = list(map(lambda x: x/len(txt_z_par), input_z[4]))
    return input_z


# In[13]:


#Language coincidence of a given text
def lang_coincidence(file_name, lang):
    z = [None] * 5
    input_z = input_z_create(file_name, lang)
    pos = langs.index(lang)
    z[0] = 5 - (abs(langs_avg_len[pos] - input_z[0]))
    z[1] = 0
    for i in range(len(input_z[1])):
        for j in range(len(freq_words[pos])):
            if input_z[1][i] == freq_words[pos][j]:
                z[1] = z[1] + 5 - abs(i+1-(j+1))
    if z[1] < 0: z[1] = 0
    if z[1] > 30: z[1] = 30
    total = 0
    for i in range(3):
        for j in range(3):
            total = total + abs(input_z[2][i][j] - rel_freqs[pos][i][j])
    z[2] = 25 - total*30
    total = 0
    for i in range(3):
        for j in range(3):
            total = total + abs(input_z[3][i][j] - rel_cond_freqs[pos][i][j])
    z[3] = 25 - total*10
    total = 0
    for i in range(3):
        total = total + abs(input_z[4][i] - consec[pos][i])
    z[4] = 15 - total*100
    return z

# In[ ]:




