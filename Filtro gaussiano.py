# UNIVERSIDAD NACIONAL DE TRUJILLO
# INGENIERIA MECATRONICA
# PROCESAMIENTO DE SEÑALES E IMAGENES

# GRUPO 01
# ELABORADO POR:
# FERREL ALFARO KEYAR RAUL
# MENDOZA PASCUAL LADY ALEXANDRA
# RODRIGUEZ VENTURA CLEVEX MAILZO

# ------------------------------------------------------------------------------

import numpy as np  # Manejo de arrays
import matplotlib.pyplot as plt  # Visualizacion
import sounddevice as sd
import soundfile as sf
plt.style.use(['dark_background'])  # Para gráficas con temas oscuros

audio = 'AUDIO_LAB_01.wav'  # Nombre del audio
data, fs = sf.read(audio)  # Leer la señal del audio

# ------------------------------------------------------------------------------

fm = fs  # Frecuencia de muestreo en Hz obtenida del audio
t = np.arange(0, 3.065, 1 / fm)  # Vector tiempo
n = len(t)  # Numero de muestras en T
señal = data  # Señal obtenida del audio
amplitud_ruido = 0.3  # Escalamiento del ruido a generar
ruido = amplitud_ruido * np.random.randn(n)  # Ruido generado usando una distribucion normal
señal_ruidosa = señal + ruido  # Señal ruidosa

# Reproduccion de audios (opcional)

# print("\n Reproduccion de AUDIO ORIGINAL (señal original) ...")
# sd.play(data,fs)                            # Reproducir el audio original
# status = sd.wait()
# print("\n Reproduccion de RUIDO (ruido generado) ...")
# sd.play(ruido,fs)                           # Reproducir el ruido
# status = sd.wait()
# print("\n Reproduccion de AUDIO CON RUIDO (señal ruidosa) ...")
# sd.play(señal_ruidosa,fs)                   # Reproducir la señal ruidosa
# status = sd.wait()

# Ploteamos la señal y el ruido

plt.subplots(1, 2, figsize=(20, 4))

plt.subplot(121)
plt.plot(t, señal)
plt.title("Señal de audio")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.subplot(122)
plt.plot(t, ruido)
plt.title("Ruido con distribucion normal generada")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

# Ploteamos la señal ruidosa y señal ruidosa-original

plt.subplots(1, 2, figsize=(20, 4))

plt.subplot(121)
plt.plot(t, señal_ruidosa)
plt.title("Señal ruidosa")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.subplot(122)
plt.plot(t, señal_ruidosa, "r", label="Señal ruidosa")
plt.plot(t, señal, "b", label="Señal original")
plt.title("Señal ruidosa - Señal original")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.show()

# ------------------------------------------------------------------------------

"""Creacion de filtro gaussiano"""
FWHM = 25  # Se establece un FWHM teórico de 25 ms
k = 100  # Valor para establecer el tamaño de la ventana gaussiana 2*k =200
gt = 1000 * np.arange(-k, k) / fm  # tiempo normalizado de la función gaussiana en ms
filtro_gaussiano = np.exp(- (4 * np.log(2) * gt ** 2) / FWHM ** 2)  # Creacion del filtro gaussiano
filtro_gaussiano_normalizado = filtro_gaussiano / np.sum(filtro_gaussiano)  # Normalizado de la ganancia a 1
ind_flanco_bajada = k + np.argmin((filtro_gaussiano[k:] - .5) ** 2)  # Indice de la mitad del flanco de subida
ind_flanco_subida = np.argmin((filtro_gaussiano - .5) ** 2)  # Indice de la mitad del flanco de subida
FWHM_calculado = gt[ind_flanco_subida] - gt[ind_flanco_bajada]  # Duración del FWHM en ms

FWHM_calculado = round(FWHM_calculado)
"""Mostrando el filtro gaussiano construido"""

plt.subplots(1, 2, figsize=(15, 4))

plt.subplot(121)
plt.plot(gt, filtro_gaussiano, label="Filtro Gaussiano")  # Gráfica de la función gaussiana construida
plt.plot([gt[ind_flanco_subida], gt[ind_flanco_bajada]],
         [filtro_gaussiano[ind_flanco_subida], filtro_gaussiano[ind_flanco_bajada]], label="FWHM")
plt.title(f"Filtro Gaussiano con FWHM teórico de {FWHM}-ms. Logrado {FWHM_calculado}-ms")
plt.xlabel("Tiempo(ms)")
plt.ylabel("Ganancia")
plt.grid()
plt.legend()

plt.subplot(122)
plt.plot(gt, filtro_gaussiano_normalizado,
         label="Filtro Gaussiano Normalizado")  # Gráfica de la función gaussiana construida
plt.plot([gt[ind_flanco_subida], gt[ind_flanco_bajada]],
         [filtro_gaussiano_normalizado[ind_flanco_subida], filtro_gaussiano_normalizado[ind_flanco_bajada]],
         label="FWHM")
plt.title(f"Filtro Gaussiano Normalizado con FWHM teórico de {FWHM}-ms. Logrado {FWHM_calculado}-ms")
plt.xlabel("Tiempo(ms)")
plt.ylabel("Ganancia")
plt.grid()
plt.legend()

plt.show()

"""Aplicación del filtro gaussiano"""
sen_filtrada_gauss = np.zeros_like(señal_ruidosa)
# El orden del filtro es 2*K = 200
for i in range(k + 1, n - k - 1):
    sen_filtrada_gauss[i] = np.sum(señal_ruidosa[i - k:i + k] * filtro_gaussiano_normalizado)

"""Mostrando los resultados"""
plt.subplots(1, 3, figsize=(20, 4))

plt.subplot(131)
plt.plot(t, señal_ruidosa, label="Señal ruidosa")
plt.plot(t, sen_filtrada_gauss, "r", label="Señal filtrada")
plt.title(f"Filtro Gaussiano con FWHM = {FWHM_calculado}-ms")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(132)
plt.plot(t, señal, "b", label="Señal original")
plt.plot(t, sen_filtrada_gauss, "r", label="Señal filtrada")
plt.title(f'Comparacion señal original con la señal filtrada')
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(133)
plt.plot(t, señal, "b", label="Señal original")
plt.plot(t, sen_filtrada_gauss, "r", label="Señal filtrada")
plt.title(f"Efecto de borde con el filtro Gaussiano con FWHM = {FWHM_calculado}-ms")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.axis([0, 0.5, -2, 2])
plt.grid()
plt.legend()
plt.show()



# Reproduccion de audios (opcional)

print("\n Reproduccion de AUDIO ORIGINAL (señal original) ...")
sd.play(data,fs)                            # Reproducir el audio original
status = sd.wait()
print("\n Reproduccion de RUIDO (ruido generado) ...")
sd.play(ruido,fs)                           # Reproducir el ruido
status = sd.wait()
print("\n Reproduccion de AUDIO CON RUIDO (señal ruidosa) ...")
sd.play(señal_ruidosa,fs)                   # Reproducir la señal ruidosa
status = sd.wait()
print("\n Reproduccion de AUDIO FILTRADO (filtro gaussiano) ...")
sd.play(sen_filtrada_gauss,fs)                   # Reproducir la señal ruidosa
status = sd.wait()