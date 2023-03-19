import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
st.set_option('deprecation.showPyplotGlobalUse', False)
# change style plt
plt.style.use('seaborn-whitegrid')

st.title("Final Project - Optimasi Pemilihan Tempat Makan Ketika Pasangan Mengatakan Terserah")

st.write("Ketika seseorang mengatakan 'terserah' dalam hal preferensi makanan, artinya mereka tidak memiliki preferensi khusus dan ingin menyerahkan keputusan kepada orang lain. Dalam hal ini, preferensi makanan dapat bervariasi tergantung pada individu dan situasi. Beberapa orang mungkin lebih memilih suasana tempat makanan, sementara yang lain mungkin lebih fleksibel dalam memilih jenis makanan. Oleh karena itu, penting untuk berkomunikasi dengan baik dengan pasangan Anda untuk mengetahui preferensi makanan mereka dan memilih restoran yang memenuhi preferensi tersebut.")
st.write("'Terserah' adalah sebuah jawaban yang diberikan oleh pasangan ketika ditanya tentang keinginan atau pilihan makanan. Dalam konteks optimasi pemilihan tempat makan, jawaban 'Terserah' menunjukkan ketidaktahuan atau ketidakpastian dalam memilih tempat makan, dan ini dapat menjadi tantangan bagi pasangan untuk menentukan tempat makan yang diinginkan. Sebagai solusi, optimasi pemilihan tempat makan dapat membantu pasangan dalam memilih tempat makan yang sesuai dengan preferensi mereka, dengan mempertimbangkan faktor-faktor seperti jenis makanan, jarak, harga, rating, suasana, diskon, menu, pasangan, entertainment, keramaian, sajian, dan konsep. Dengan demikian, pasangan dapat menikmati makanan di tempat makan yang disukai, tanpa perlu merasa bingung atau kebingungan dalam memilih tempat makan.")
# 1. Membaca Dataset
st.header("1. Dataset")
df = pd.read_csv('places_to_eat_in_the_jogja_region.csv')
st.write(df)

restoran = df.values.tolist()

# 2. Normalisasi
colnames = ['nama', 'jenis', 'jarak', 'harga', 'rating', 'suasana', 'diskon', 'menu', 'pasangan', 'entertainment', 'keramaian', 'sajian', 'konsep']
df = pd.DataFrame(restoran, columns=colnames)
df_original = df.copy()
df['jarak'] = df['jarak'].str.extract('(\d+\.\d+)').astype(float)
df['harga'] = df['harga'].astype(int)
df['rating'] = df['rating'].astype(float)
df['entertainment'] = df['entertainment'].astype(int)
df['keramaian'] = df['keramaian'].astype(int)


def label_encoding(dataframe, column):
    unique_values = dataframe[column].unique()
    for i, value in enumerate(unique_values):
        dataframe.loc[dataframe[column] == value, column] = i
def min_max_normalization(dataframe, column):
    dataframe[column] = (dataframe[column] - dataframe[column].min()) / (dataframe[column].max() - dataframe[column].min())
    
def count_words_separator(text, separator):
    return len(text.split(separator))

def distance_to_category(distance):
    if distance <= 1:
        return 5
    elif distance <= 2:
        return 4
    elif distance <= 3:
        return 3
    elif distance <= 4:
        return 2
    elif distance <= 5:
        return 1
    else:
        return 0

def price_to_category(price):
    if price >= 10000 and price < 42000:
        return 4
    elif price >= 42000 and price < 74000:
        return 3
    elif price >= 74000 and price < 106000:
        return 2
    elif price >= 106000 and price < 138000:
        return 1
    elif price >= 138000:
        return 0
    
def rating_to_category(rating):
    if rating >= 4.0:
        return 0
    elif rating >= 3.0:
        return 1
    elif rating >= 2.0:
        return 2
    elif rating >= 1.0:
        return 3
    else:
        return 4
    
label_encoding(df, 'jenis')
df['jarak'] = df['jarak'].apply(lambda x: distance_to_category(x))
df['harga'] = df['harga'].apply(lambda x: price_to_category(x))
df['rating'] = df['rating'].apply(lambda x: rating_to_category(x))
label_encoding(df, 'suasana')
label_encoding(df, 'diskon')
df['menu'] = df['menu'].apply(lambda x: count_words_separator(x, ','))
label_encoding(df, 'pasangan')
label_encoding(df, 'sajian')
label_encoding(df, 'konsep')

st.header("2. Data Setelah Normalisasi")
st.write(df)

# 3. Input Preferensi Makanan
# input selection
st.header("3. Input Preferensi Makanan")
jenis = st.selectbox('Jenis Makanan', df_original.jenis.unique())
suasana = st.selectbox('Suasana', df_original.suasana.unique())
pasangan = st.selectbox('Pasangan', df_original.pasangan.unique())
entertainment = st.selectbox('Entertainment', ["Banyak", "Sedikit"])
keramaian = st.selectbox('Keramaian', ["Ramai", "Sepi"])
sajian = st.selectbox('Sajian', df_original.sajian.unique())
konsep = st.selectbox('Konsep', df_original.konsep.unique())

def label_encoder_with_priority(col, priority):
    unique_values = df_original[col].unique()
    encoded_values = {}
    for i, value in enumerate(unique_values):
        if value == priority:
            encoded_values[value] = len(unique_values) - 1
        else:
            encoded_values[value] = i - 1
            if encoded_values[value] == -1:
                encoded_values[value] = 0
    return df_original[col].apply(lambda x: encoded_values[x])

def label_encoder_with_priority_entertainment(col, priority):
    unique_values = df_original[col].unique()
    encoded_values = {}
    if priority == "Sedikit":
        for i, value in enumerate(unique_values):
            encoded_values[value] = i
    else:
        for i, value in enumerate(unique_values):
            encoded_values[value] = len(unique_values) - 1 - i
    return df_original[col].apply(lambda x: encoded_values[x])

def label_encoder_with_priority_keramaian(col, priority):
    unique_values = df_original[col].unique()
    encoded_values = {}
    if priority == "Sepi":
        for i, value in enumerate(unique_values):
            encoded_values[value] = i
    else:
        for i, value in enumerate(unique_values):
            encoded_values[value] = len(unique_values) - 1 - i
    return df_original[col].apply(lambda x: encoded_values[x])

df['jenis'] = label_encoder_with_priority('jenis', jenis)
df['suasana'] = label_encoder_with_priority('suasana', suasana)
df['pasangan'] = label_encoder_with_priority('pasangan', pasangan)
df['entertainment'] = label_encoder_with_priority_entertainment('entertainment', entertainment)
df['keramaian'] = label_encoder_with_priority_keramaian('keramaian', keramaian)
df['sajian'] = label_encoder_with_priority('sajian', sajian)
df['konsep'] = label_encoder_with_priority('konsep', konsep)

st.header("4. Data Setelah Update Preferensi")
st.write(df)


# Implementasi Algoritma Genetika

st.header("5. Implementasi Algoritma Genetika")
# Definisi Parameter GA (Genetic Algorithm)
POPULATION_SIZE = 20
GENERATIONS = 200
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1

# 1. Inisialisasi Populasi
population = []
for i in range(POPULATION_SIZE):
    chromosome = random.sample(range(len(df)), 12)
    population.append(chromosome)
    
data = df.values.tolist()

# 2. Membuat Fungsi Fitness
# fungsi fitness jenis	jarak	harga	rating	suasana	diskon	menu	pasangan	entertainment	keramaian	sajian	konsep
def fitness(solution, show=False, k=0):
    score = 0
    bobot = {
        "jenis": 0.5,
        "jarak": 0.8,
        "harga": 0.8,
        "rating": 0.5,
        "suasana": 0.5,
        "diskon": 0.5,
        "menu": 0.1,
        "pasangan": 1,
        "entertainment": 0.5,
        "keramaian": 0.5,
        "sajian": 0.5,
        "konsep": 0.5
    }
    if show and k == 0 or k == 1:
        st.subheader("Sampel Solusi atau Individu (ID Resto) " + str(k+1) + ":")
        df_sample_solution = pd.DataFrame(solution).T
        # raname columns and name Gen 1 to Gen 12
        df_sample_solution.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
        # rename index to individual or solution
        df_sample_solution.index = ["Individu " + str(k+1)]
        
        st.dataframe(df_sample_solution)
        
    tmp_bobot = {}
    new_columns = ["bobot_jenis", "bobot_jarak", "bobot_harga", "bobot_rating", "bobot_suasana", "bobot_diskon", "bobot_menu", "bobot_pasangan", "bobot_entertainment", "bobot_keramaian", "bobot_sajian", "bobot_konsep"]
    for i in solution:
        score += bobot["jenis"] * data[i][1]
        score += bobot["jarak"] * data[i][2]
        score += bobot["harga"] * data[i][3]
        score += bobot["rating"] * data[i][4]
        score += bobot["suasana"] * data[i][5]
        score += bobot["diskon"] * data[i][6]
        score += bobot["menu"] * data[i][7]
        score += bobot["pasangan"] * data[i][8]
        score += bobot["entertainment"] * data[i][9]
        score += bobot["keramaian"] * data[i][10]
        score += bobot["sajian"] * data[i][11]
        score += bobot["konsep"] * data[i][12]
        if show and k == 0 or k == 1:
            tmp_bobot[i] = dict(zip(pd.DataFrame(data).columns, pd.DataFrame(data).loc[i].values))
            tmp_bobot[i]["bobot_jenis"] = bobot["jenis"] * data[i][1]
            tmp_bobot[i]["bobot_jarak"] = bobot["jarak"] * data[i][2]
            tmp_bobot[i]["bobot_harga"] = bobot["harga"] * data[i][3]
            tmp_bobot[i]["bobot_rating"] = bobot["rating"] * data[i][4]
            tmp_bobot[i]["bobot_suasana"] = bobot["suasana"] * data[i][5]
            tmp_bobot[i]["bobot_diskon"] = bobot["diskon"] * data[i][6]
            tmp_bobot[i]["bobot_menu"] = bobot["menu"] * data[i][7]
            tmp_bobot[i]["bobot_pasangan"] = bobot["pasangan"] * data[i][8]
            tmp_bobot[i]["bobot_entertainment"] = bobot["entertainment"] * data[i][9]
            tmp_bobot[i]["bobot_keramaian"] = bobot["keramaian"] * data[i][10]
            tmp_bobot[i]["bobot_sajian"] = bobot["sajian"] * data[i][11]
            tmp_bobot[i]["bobot_konsep"] = bobot["konsep"] * data[i][12]
            tmp_bobot[i]["score"] = score
        
    if show and k == 0 or k == 1:
        st.subheader("Kromosom, Bobot, dan Nilai Fitness " + str(k+1) + ":")
        df_tmp_bobot = pd.DataFrame(tmp_bobot).T
        # rename columns index 0 to name
        df_tmp_bobot.columns = ["nama", "jenis", "jarak", "harga", "rating", "suasana", "diskon", "menu", "pasangan", "entertainment", "keramaian", "sajian", "konsep"] + new_columns + ["score"]
        st.dataframe(df_tmp_bobot)
    return score


fitness_scores_for_plot = []
for generation in range(GENERATIONS):
    if generation == 0 or generation == 1:
        st.title("Generasi " + str(generation+1))
    if generation == 0 or generation == 1:
        st.subheader("5.1 Populasi Awal")
        df_population = pd.DataFrame(population)
        df_population.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
        df_population.index = ["Individu " + str(i+1) for i in range(20)]
        st.dataframe(df_population, 2000)

    # hitung nilai fitness untuk setiap kromosom
    fitness_scores = []     
    if generation == 0 or generation == 1:
        for index, chromosome in enumerate(population):
            fitness_scores.append((chromosome, fitness(chromosome, True, index)))
            
    else:
        for index, chromosome in enumerate(population):
            fitness_scores.append((chromosome, fitness(chromosome)))  

    fitness_scores_for_plot.append(max(fitness_scores, key=lambda x: x[1])[1])
    
    
    # check apakah sudah mencapai nilai fitness maksimum atau convergen
    if generation > 50:
        if fitness_scores_for_plot[generation] == fitness_scores_for_plot[generation-50]:
            st.write("Solusi ditemukan pada generasi ke-" + str((generation-50)+1))
            st.write("Solusi: " + str(max(fitness_scores, key=lambda x: x[1])[0]))
            st.write("Nilai Fitness: " + str(max(fitness_scores, key=lambda x: x[1])[1]))
            break
    # # sort kromosom berdasarkan nilai fitness terbesar
    # fitness_scores.sort(key=lambda x: x[1], reverse=True)
    if generation == 0 or generation == 1:
        df_fitness_scores = pd.DataFrame(fitness_scores)
        df_fitness_scores.columns = ["Individu", "Nilai Fitness"]
        st.dataframe(df_fitness_scores, 2000)

    # seleksi turnamen untuk memilih kromosom terbaik
    selected = []
    for i in range(POPULATION_SIZE):
        tournament = random.sample(fitness_scores, 3)
        tournament.sort(key=lambda x: x[1], reverse=True)
        selected.append(tournament[0][0])
        
    if generation == 0 or generation == 1:
        st.subheader("5.2 Seleksi Turnamen")
        df_selected = pd.DataFrame(selected)
        df_selected.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
        df_selected.index = ["Individu " + str(i+1) for i in range(20)]
        st.dataframe(df_selected, 2000)

    # rekombinasi dengan crossover satu titik
    new_population = []
    number_recombination = 0
    if generation == 0 or generation == 1:
        st.subheader("5.3 Rekombinasi atau Crossover")
    for i in range(0, POPULATION_SIZE, 2):
        parent1 = selected[i]
        parent2 = selected[i+1]
        random_number = random.random()
        if random_number < CROSSOVER_RATE:
            if generation == 0 or generation == 1:
                st.write("Masuk Ke Kondisi Dengan Nilai Random", random_number, "Lebih Kecil Dari", CROSSOVER_RATE, "")
            crossover_point = random.randint(1, len(parent1)-1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
        else:
            if generation == 0 or generation == 1:
                st.write("Masuk Ke Kondisi Dengan Nilai Random", random_number, "Lebih Besar Dari", CROSSOVER_RATE, "")
            child1 = parent1
            child2 = parent2
        if generation == 0 or generation == 1:
            st.write("Rekombinasi Menggunakan Single Point Crossover Ke-", number_recombination+1)
            df_marge = pd.DataFrame([parent1, parent2, child1, child2])
            df_marge = df_marge.rename({0: 'Parent 1', 1: 'Parent 2', 2: 'Child / Offspring 1', 3: 'Child / Offspring 2'})
            df_marge.columns = ["Gen " + str(i+1) for i in range(12)]
            st.table(df_marge)

        new_population.append(child1)
        new_population.append(child2)
        number_recombination += 1
    if generation == 0 or generation == 1:
        st.subheader("5.4 Mutasi")
    # mutasi dengan swap dua gen
    for i in range(len(new_population)):
        random_number = random.random()
        if random_number < MUTATION_RATE:
            mutate_point1 = random.randint(0, len(new_population[i])-1)
            mutate_point2 = random.randint(0, len(new_population[i])-1)
            new_population[i][mutate_point1], new_population[i][mutate_point2] = new_population[i][mutate_point2], new_population[i][mutate_point1]
            if generation == 0 or generation == 1:
                st.write("Mutasi Dilakukan Pada Kromosom Ke-", i+1, "Dengan Nilai Random", random_number, "Lebih Kecil Dari", MUTATION_RATE, "")
                st.write("Mutasi Swap Gen Ke-", mutate_point1+1, "Dengan Gen Ke-", mutate_point2+1)
                df_mutate = pd.DataFrame([new_population[i]])
                df_mutate.columns = ["Gen " + str(i+1) for i in range(12)]
                df_mutate.index = ["Kromosom " + str(i+1)]
                st.dataframe(df_mutate, 2000)
    
    # ganti populasi lama dengan populasi baru
    population = new_population

# cari kromosom terbaik setelah iterasi selesai
best_chromosome = max(population, key=lambda x: fitness(x))


# fitness_scores_for_plot start from 1
plot_fitness_scores = { }

for i in range(len(fitness_scores_for_plot)):
    plot_fitness_scores[i+1] = fitness_scores_for_plot[i]

plt.plot(list(plot_fitness_scores.keys()), list(plot_fitness_scores.values()))
plt.xlabel("Generasi")
plt.ylabel("Nilai Fitness")
plt.title("Grafik Nilai Fitness Terhadap Generasi")
st.pyplot()

st.table(pd.DataFrame(best_chromosome).T)

rekomendasi = []
number_gen = 1
for i in best_chromosome:
    st.write("Gen ke-", number_gen ," : ", data[i][0])
    rekomendasi.append(data[i][0])
    number_gen += 1
    
st.title("Rekomendasi Tempat Makan Pasangan Terbaik Anda :)")
df_rekomendasi = df_original[df_original['nama'].isin(rekomendasi)]
st.dataframe(df_rekomendasi)
