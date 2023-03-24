import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
st.set_option('deprecation.showPyplotGlobalUse', False)
# Mengubah Style Matplotlib
plt.style.use('seaborn-whitegrid')

# Menampilkan Text Untuk Memberikan Informasi
st.title("Final Project - Optimasi Pemilihan Tempat Makan Ketika Pasangan Mengatakan Terserah")
st.write("Ketika seseorang mengatakan 'terserah' dalam hal preferensi makanan, artinya mereka tidak memiliki preferensi khusus dan ingin menyerahkan keputusan kepada orang lain. Dalam hal ini, preferensi makanan dapat bervariasi tergantung pada individu dan situasi. Beberapa orang mungkin lebih memilih suasana tempat makanan, sementara yang lain mungkin lebih fleksibel dalam memilih jenis makanan. Oleh karena itu, penting untuk berkomunikasi dengan baik dengan pasangan Anda untuk mengetahui preferensi makanan mereka dan memilih restoran yang memenuhi preferensi tersebut.")
st.write("'Terserah' adalah sebuah jawaban yang diberikan oleh pasangan ketika ditanya tentang keinginan atau pilihan makanan. Dalam konteks optimasi pemilihan tempat makan, jawaban 'Terserah' menunjukkan ketidaktahuan atau ketidakpastian dalam memilih tempat makan, dan ini dapat menjadi tantangan bagi pasangan untuk menentukan tempat makan yang diinginkan. Sebagai solusi, optimasi pemilihan tempat makan dapat membantu pasangan dalam memilih tempat makan yang sesuai dengan preferensi mereka, dengan mempertimbangkan faktor-faktor seperti jenis makanan, jarak, harga, rating, suasana, diskon, menu, pasangan, entertainment, keramaian, sajian, dan konsep. Dengan demikian, pasangan dapat menikmati makanan di tempat makan yang disukai, tanpa perlu merasa bingung atau kebingungan dalam memilih tempat makan.")

# Membuat Dataframe Untuk Menampilkan Atribut yang Dipilih
df_feature = pd.DataFrame(columns=['Atribut'])
df_feature.loc[0] = ['Jenis Makanan']
df_feature.loc[1] = ['Jarak']
df_feature.loc[2] = ['Harga']
df_feature.loc[3] = ['Rating']
df_feature.loc[4] = ['Suasana']
df_feature.loc[5] = ['Diskon']
df_feature.loc[6] = ['Menu']
df_feature.loc[7] = ['Pasangan']
df_feature.loc[8] = ['Entertainment']
df_feature.loc[9] = ['Keramaian']
df_feature.loc[10] = ['Sajian']
df_feature.loc[11] = ['Konsep']
df_feature.index = df_feature.index + 1
st.dataframe(df_feature, width=2000)

# 1. Membaca Dataset
st.header("1. Dataset")
df = pd.read_csv('places_to_eat_in_the_jogja_region.csv')
st.write(df)
df_jenis = str(df['Preferensi Makanan'].unique().tolist())
df_jarak = df['Lokasi Restoran'].unique().tolist()
df_harga = df['Harga Rata-Rata Makanan di Toko (Rp)'].unique().tolist()
df_rating = df['Rating Toko'].unique().tolist()
df_suasana = str(df['Jenis Suasana'].unique().tolist())
df_diskon = str(df['Toko Sering Diskon (Ya/Tidak)'].unique().tolist())
df_menu = str(df['Variasi Makanan'].unique().tolist())
df_pasangan = str(df['Pelayanan Khusus Pasangan (Ya/Tidak)'].unique().tolist())
df_entertainment = str(df['Entertainment'].unique().tolist())
df_keramaian = str(df['Keramaian Restoran'].unique().tolist())
df_sajian = str(df['Disajikan atau Ambil Sendiri'].unique().tolist())
df_konsep = str(df['All You Can Eat atau Ala Carte'].unique().tolist())
df_menu = df_menu.replace('[', '')
df_menu = df_menu.replace(']', '')
df_menu = df_menu.replace("'", '')
df_menu = df_menu.split(', ')
df_menu = str(list(dict.fromkeys(df_menu)))
st.write("1. Jenis Makanan: ", df_jenis)
st.write("2. Range Jarak: ", min(df_jarak), '-', max(df_jarak))
st.write("3. Range Harga (Rp): ", min(df_harga), '-', max(df_harga))
st.write("4. Range Rating: ", min(df_rating), '-', max(df_rating))
st.write("5. Jenis Suasana: ", df_suasana)
st.write("6. Diskon: ", df_diskon)
st.write("7. Menu: ", df_menu)
st.write("8. Pasangan: ", df_pasangan)
st.write("9. Jumlah Entertaiment", df_entertainment)
st.write("10. Keramaian (Ramai, Sedang, Sepi): ", df_keramaian)
st.write("11. Sajian : ", df_sajian)
st.write("12. Konsep: ", df_konsep)
restoran = df.values.tolist() # Mengubah Dataframe ke List

# 2. Transformasi Data
colnames = ['nama', 'jenis', 'jarak', 'harga', 'rating', 'suasana', 'diskon', 'menu', 'pasangan', 'entertainment', 'keramaian', 'sajian', 'konsep'] # Membuat list untuk nama kolom
df = pd.DataFrame(restoran, columns=colnames) # Membuat dataframe baru dengan nama kolom yang telah dibuat
df_original = df.copy() # Membuat dataframe baru untuk menyimpan dataframe asli
df['jarak'] = df['jarak'].str.extract('(\d+\.\d+)').astype(float) # Mengubah tipe data jarak dari string ke float
df['harga'] = df['harga'].astype(int) # Mengubah tipe data harga dari string ke integer
df['rating'] = df['rating'].astype(float) # Mengubah tipe data rating dari string ke float
df['entertainment'] = df['entertainment'].astype(int) # Mengubah tipe data entertainment dari string ke integer
df['keramaian'] = df['keramaian'].astype(int) # Mengubah tipe data keramaian dari string ke integer


# Berfungsi untuk mengubah nilai atribut menjadi angka
def label_encoding(dataframe, column):
    unique_values = dataframe[column].unique()
    for i, value in enumerate(unique_values):
        dataframe.loc[dataframe[column] == value, column] = i
# Berfungsi untuk menghitung jumlah kata dalam suatu kalimat
def count_words_separator(text, separator):
    return len(text.split(separator))
# Berfungsi untuk mengubah nilai atribut jarak menjadi kategori (Reprentasi Numerik)
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
# Berfungsi untuk mengubah nilai atribut harga menjadi kategori (Reprentasi Numerik)
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
# Berfungsi untuk mengubah nilai atribut rating menjadi kategori (Reprentasi Numerik)
def rating_to_category(rating):
    if rating >= 4.0:
        return 4
    elif rating >= 3.0:
        return 3
    elif rating >= 2.0:
        return 2
    elif rating >= 1.0:
        return 1
    else:
        return 0

# Menerapkan Masing-Masing Fungsi Kedalam Atribut
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

st.header("2. Data Setelah Transformasi")
st.write("Masing-masing atribut akan diubah menjadi representasi numerik yang bersifat kategorikal atau nominal misalnya jenis makanan akan diubah menjadi angka 0, 1, 2, dst.")
st.write(df)

# 3. Input Preferensi Makanan
# input selection
st.header("3. Input Preferensi Makanan")
st.write("Pemilihan preferensi makanan bertujuan untuk menentukan restoran mana yang cocok dengan preferensi makanan yang dimiliki pasangan. memasukkan preferensi makanan pengguna ke dalam algoritma genetika juga dapat membantu menghasilkan solusi yang lebih personal dan menyesuaikan dengan kebutuhan pengguna")
jenis = st.selectbox('Jenis Makanan', df_original.jenis.unique())
suasana = st.selectbox('Suasana', df_original.suasana.unique())
pasangan = st.selectbox('Pasangan', df_original.pasangan.unique())
entertainment = st.selectbox('Entertainment', ["Banyak", "Sedikit"])
keramaian = st.selectbox('Keramaian', ["Ramai", "Sepi"])
sajian = st.selectbox('Sajian', df_original.sajian.unique())
konsep = st.selectbox('Konsep', df_original.konsep.unique())
st.write("Ketika selesai memilih preferensi makanan, data akan ditransformasi menjadi representasi numerik yang bersifat ordinal yang dimana nilai atribut akan diurutkan berdasarkan prioritas yang telah ditentukan")


# Berfungsi untuk mengubah nilai atribut menjadi angka dengan prioritas tertentu
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

# Berfungsi untuk mengubah nilai atribut menjadi angka dengan prioritas tertentu
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


# Berfungsi untuk mengubah nilai atribut menjadi angka dengan prioritas tertentu
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

# Menerapkan Masing-Masing Fungsi Kedalam Atribut
df['jenis'] = label_encoder_with_priority('jenis', jenis)
df['suasana'] = label_encoder_with_priority('suasana', suasana)
df['pasangan'] = label_encoder_with_priority('pasangan', pasangan)
df['entertainment'] = label_encoder_with_priority_entertainment('entertainment', entertainment)
df['keramaian'] = label_encoder_with_priority_keramaian('keramaian', keramaian)
df['sajian'] = label_encoder_with_priority('sajian', sajian)
df['konsep'] = label_encoder_with_priority('konsep', konsep)

# 4. Data Setelah Update Preferensi
st.header("4. Data Setelah Update Preferensi")
st.write(df)


# 5. Implementasi Algoritma Genetika
st.header("5. Implementasi Algoritma Genetika")
# Definisi Parameter GA (Genetic Algorithm)
POPULATION_SIZE = 20
GENERATIONS = 300
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
CONVERGENCE_THRESHOLD = 50
st.write("POPULATION_SIZE = ", POPULATION_SIZE)
st.write("GENERATIONS = ", GENERATIONS)
st.write("CROSSOVER_RATE = ", CROSSOVER_RATE)
st.write("MUTATION_RATE = ", MUTATION_RATE)
st.write("CONVERGENCE_THRESHOLD = ", CONVERGENCE_THRESHOLD)

# 1. Inisialisasi Populasi
population = []
for i in range(POPULATION_SIZE):
    chromosome = random.sample(range(len(df)), 12) # Membuat 12 Individu dari 12 Restoran (ID Resto 0 - 290)
    population.append(chromosome)
    
data = df.values.tolist() # Mengubah Dataframe menjadi list

# 2. Membuat Fungsi Fitness
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
        df_sample_solution.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
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
        st.write("Bobot yang digunakan adalah sebagai berikut: ", str(bobot), " dan setiap bobot akan dikalikan dengan nilai kriteria yang ada pada setiap individu (restoran).")
        df_tmp_bobot = pd.DataFrame(tmp_bobot).T
        df_tmp_bobot.columns = ["nama", "jenis", "jarak", "harga", "rating", "suasana", "diskon", "menu", "pasangan", "entertainment", "keramaian", "sajian", "konsep"] + new_columns + ["score"]
        st.dataframe(df_tmp_bobot)
    return score


fitness_scores_for_plot = [] # Variabel Untuk Menyimpan Nilai Fitness
for generation in range(GENERATIONS): # Looping Generasi
    if generation == 0 or generation == 1:
        st.title("Generasi " + str(generation+1))
    if generation == 0 or generation == 1:
        st.subheader("5.1 Populasi Awal")
        st.write("Populasi awal adalah kumpulan solusi yang dihasilkan secara acak. Pada kasus ini, solusi yang dihasilkan adalah 20 individu yang terdiri dari 12 gen. Setiap gen memiliki nilai 0-290 (secara acak) yang merepresentasikan ID Restoran.")
        st.write("Misalkan, Pada Individu 1 pada Gen 1", population[0][0], " Yang merupakan data dari Restoran", data[population[0][0]][0])
        df_population = pd.DataFrame(population)
        df_population.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
        df_population.index = ["Individu " + str(i+1) for i in range(20)]
        st.dataframe(df_population, 2000)

    fitness_scores = []     
    if generation == 0 or generation == 1:
        for index, chromosome in enumerate(population):
            fitness_scores.append((chromosome, fitness(chromosome, True, index)))
            
    else:
        for index, chromosome in enumerate(population):
            fitness_scores.append((chromosome, fitness(chromosome)))  

    fitness_scores_for_plot.append(max(fitness_scores, key=lambda x: x[1])[1])
    
    # Mengecek Apakah Generasi Lebih Dari 50 dan Apakah Nilai Fitness Sama Dengan 50 Generasi Sebelumnya, Jika Ya Maka Solusi Ditemukan
    if generation > 50:
        if fitness_scores_for_plot[generation] == fitness_scores_for_plot[generation-CONVERGENCE_THRESHOLD]:
            st.write("Solusi ditemukan pada generasi ke-" + str((generation-CONVERGENCE_THRESHOLD)+1))
            st.write("Solusi: " + str(max(fitness_scores, key=lambda x: x[1])[0]))
            st.write("Nilai Fitness: " + str(max(fitness_scores, key=lambda x: x[1])[1]))
            break

    if generation == 0 or generation == 1:
        df_fitness_scores = pd.DataFrame(fitness_scores)
        df_fitness_scores.columns = ["GEN", "Nilai Fitness"]
        df_fitness_scores.index = ["Individu " + str(i+1) for i in range(20)]
        st.subheader("5.2 Menghitung Nilai Fitness")
        st.write("Nilai Fitness adalah hasil perkalian antara bobot dan nilai kriteria yang ada pada setiap individu (restoran) kemudian dijumlahkan setiap ID Restoran.")
        st.dataframe(df_fitness_scores, 2000)

    # Seleksi Turnamen Untuk Mendapatkan Individu Terbaik
    selected = []
    for i in range(POPULATION_SIZE):
        tournament = random.sample(fitness_scores, 3)
        tournament.sort(key=lambda x: x[1], reverse=True)
        selected.append(tournament[0][0])
        
    if generation == 0 or generation == 1:
        st.subheader("5.3 Seleksi Turnamen")
        st.write("Seleksi turnamen adalah proses seleksi yang dilakukan dengan cara memilih individu terbaik dari 3 individu secara acak. Pada kasus ini, individu terbaik adalah individu dengan nilai fitness terbesar kemudian individu tersebut akan dipilih untuk menjadi parent untuk proses rekombinasi.")
        df_selected = pd.DataFrame(selected)
        df_selected.columns = ["ID Resto (GEN) " + str(i+1) for i in range(12)]
        df_selected.index = ["Individu " + str(i+1) for i in range(20)]
        st.dataframe(df_selected, 2000)

    # rekombinasi dengan crossover satu titik
    new_population = []
    number_recombination = 0
    random_cross_point =  random.randint(1, 11)
    if generation == 0 or generation == 1:
        st.subheader("5.4 Rekombinasi atau Crossover")
    for i in range(0, POPULATION_SIZE, 2): # Looping Parent Setiap 2 Individu
        parent1 = selected[i]
        parent2 = selected[i+1]
        random_number = random.random()
        if random_number < CROSSOVER_RATE:
            crossover_point = random_cross_point
            if generation == 0 or generation == 1:
                st.write("Masuk Ke Kondisi Dengan Nilai Random", random_number, "Lebih Kecil Dari", CROSSOVER_RATE, "")
                st.write("Titik Rekombinasi Pada Individu", i+1, "dan", i+2, "adalah", crossover_point, "")
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
        else:
            if generation == 0 or generation == 1:
                st.write("Masuk Ke Kondisi Dengan Nilai Random", random_number, "Lebih Besar Dari", CROSSOVER_RATE, "")
                st.write("Tidak Ada Titik Rekombinasi Pada Individu", i+1, "dan", i+2, " Dikarenakan Nilai Random Lebih Besar Dari", CROSSOVER_RATE)
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
    # Mutasi Dengan Swap Dua Gen
    for i in range(len(new_population)):
        random_number = random.random()
        if random_number < MUTATION_RATE:
            mutate_point1 = random.randint(0, len(new_population[i])-1)
            mutate_point2 = random.randint(0, len(new_population[i])-1)
            new_population[i][mutate_point1], new_population[i][mutate_point2] = new_population[i][mutate_point2], new_population[i][mutate_point1]
            if generation == 0 or generation == 1:
                st.subheader("5.5 Mutasi")
                st.write("Mutasi Dilakukan Pada Kromosom Ke-", i+1, "Dengan Nilai Random", random_number, "Lebih Kecil Dari", MUTATION_RATE, "")
                st.write("Mutasi Swap Gen Ke-", mutate_point1+1, "Dengan Gen Ke-", mutate_point2+1)
                df_mutate = pd.DataFrame([new_population[i]])
                df_mutate.columns = ["Gen " + str(i+1) for i in range(12)]
                df_mutate.index = ["Kromosom " + str(i+1)]
                st.dataframe(df_mutate, 2000)
    
    # Ganti Populasi Lama Dengan Populasi Baru
    population = new_population

# Cari Kromosom Terbaik Setelah Generasi Terakhir
best_chromosome = max(population, key=lambda x: fitness(x))

plot_fitness_scores = { }

for i in range(len(fitness_scores_for_plot)):
    plot_fitness_scores[i+1] = fitness_scores_for_plot[i]

plt.plot(list(plot_fitness_scores.keys()), list(plot_fitness_scores.values()))
plt.xlabel("Generasi")
plt.ylabel("Nilai Fitness")
plt.title("Grafik Nilai Fitness Terhadap Generasi")
st.pyplot()

st.table(pd.DataFrame(best_chromosome).T)

recomendation = []
number_gen = 1
for i in best_chromosome:
    st.write("Gen ke-", number_gen ," : ", data[i][0])
    recomendation.append(data[i][0])
    number_gen += 1
    
st.title("Rekomendasi Tempat Makan Pasangan Terbaik Anda :)")
df_rekomendasi = df_original[df_original['nama'].isin(recomendation)]
st.dataframe(df_rekomendasi)
