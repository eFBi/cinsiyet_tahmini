"""ses_ile_cinsiyet_tahmini.ipynb

# Ses ile cinsiyet tahmini

Bu çalışmada,Veri seti olarak 3168 erkek ve kadın ses örneği 
kullanılmıştır.Bunların 1584 erkek ve 1584 kadın ses örneğidir. Öncelikle veri 
incelenmiş boş satır varmı diye kontrol edilmiştir. Daha sonra verimiz test ve train
olarak bölünmüştür. Bölünen veri testimiz scaler işlemine sokularak 
normalizasyon işlemi gerçekleştirilmiştir. Daha sonra iki sınıflı cinsiyet tanıma 
uygulamasını konvolüsyonel sinir ağına sokulmuş ve % 95 lik başarılı bir sonuç 
alınmıştır.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sbn
import tensorflow as tf

"""**Veri kümesi**"""

veri = pd.read_csv('voice.csv')

veri.head(-10)

veri.isnull().sum() #verilerimizde boş değer varmı var isetoplam ne kadar?

veri.info()

plt.figure(figsize=(20,5)) #kadın erkek oranı
sbn.countplot(veri['label'])

etiket = LabelEncoder()

veri['label'] = etiket.fit_transform(veri['label'])

"""-------------------------------------------------------------------------------------------"""

dict(enumerate(etiket.classes_))

"""-------------------------------------------------------------------------------------------"""

y = veri['label'].copy()
X = veri.drop('label', axis=1).copy()

"""-------------------------------------------------------------------------------------------

**scaling :** boyutunu büyütek veya küçültmek
nöronlara vereceğimiz versisetini küçük bir hale getirmek istiyoruz ki yapacağımız işlemler daha kolay olsun hemde hızlı bir şekilde bu süreci tamamlayabilelim.

sıfır ile bir arasındaki rakamlara yuvarlama işlemi yani normalizasyon yapıyoruz.
"""

scaler = StandardScaler()

X = scaler.fit_transform(X)

"""-------------------------------------------------------------------------------------------

Elimizdeki X vektörünü matris haline getiriyoruz.
"""

X = tf.keras.preprocessing.sequence.pad_sequences(X, dtype=np.float, maxlen=25, padding='post')
X = X.reshape(-1, 5, 5)
X = np.expand_dims(X, axis=3)

"""-------------------------------------------------------------------------------------------"""

X.shape

"""-------------------------------------------------------------------------------------------"""

plt.figure(figsize=(12, 12))

for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.imshow(np.squeeze(X[i]))
    plt.axis('off')
    
plt.show()

"""Model Eğitimi"""

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)

inputs = tf.keras.Input(shape=(X.shape[1], X.shape[2], X.shape[3]))

x = tf.keras.layers.Conv2D(16, 2, activation='relu')(inputs)
x = tf.keras.layers.MaxPooling2D()(x)

x = tf.keras.layers.Conv2D(32, 1, activation='relu')(x)
x = tf.keras.layers.MaxPooling2D()(x)

x = tf.keras.layers.Flatten()(x)

x = tf.keras.layers.Dense(64, activation='relu')(x)

outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.Model(inputs, outputs)

"""-------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------
"""

model.summary()

"""-------------------------------------------------------------------------------------------"""

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.AUC(name='auc')
    ]
)

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    batch_size=32,
    epochs=100,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        )
    ]
)

"""-------------------------------------------------------------------------------------------

Model Değerlendirmemiz
"""

model.evaluate(X_test, y_test)

"""bu model de %95 oranında bir başarı elde edilmiştir."""
