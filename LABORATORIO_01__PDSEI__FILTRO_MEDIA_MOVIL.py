# UNIVERSIDAD NACIONAL DE TRUJILLO
# INGENIERIA MECATRONICA
# PROCESAMIENTO DE SEÑALES E IMAGENES

# GRUPO 01
# ELABORADO POR:
    # FERREL ALFARO KEYAR RAUL
    # MENDOZA PASCUAL LADY ALEXANDRA
    # RODRIGUEZ VENTURA CLEVEX MAILZO

#------------------------------------------------------------------------------

import numpy as np                      # Manejar arrays
import matplotlib.pyplot as plt         # Realizar graficos
import sounddevice as sd                # Reproducir audios wav
import soundfile as sf                  # Leer audios wav
plt.style.use(['dark_background'])      # Graficas con temas oscuros

#------------------------------------------------------------------------------

audio = 'AUDIO_LAB_01.wav'      # Nombre del audio
data,fs = sf.read(audio)        # Leer la señal del audio
 
#------------------------------------------------------------------------------

fm = fs                                     # Frecuencia de muestreo en Hz obtenida del audio
t = np.arange(0,3.065,1/fm)                 # Vector tiempo
n = len(t)                                  # Numero de muestras en T

señal = data                                # Señal obtenida del audio

amplitud_ruido = 0.3                        # Escalamiento del ruido a generar
ruido = amplitud_ruido*np.random.randn(n)   # Ruido generado usando una distribucion normal

señal_ruidosa = señal+ruido                 # Señal ruidosa

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

plt.subplots(1,2,figsize=(20,4))

plt.subplot(121)
plt.plot(t,señal)
plt.title("Señal de audio")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.subplot(122)
plt.plot(t,ruido)
plt.title("Ruido con distribucion normal generada")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

# Ploteamos la señal ruidosa y señal ruidosa-original

print("\n Graficas")

plt.subplots(1,2,figsize=(20,4))

plt.subplot(121)
plt.plot(t,señal_ruidosa)
plt.title("Señal ruidosa")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.subplot(122)
plt.plot(t,señal_ruidosa, "r",label="Señal ruidosa")
plt.plot(t,señal,"b",label="Señal original")
plt.title("Señal ruidosa - Señal original")
plt.xlabel("Tiempo")
plt.ylabel("Amplitud")
plt.grid()

plt.show()

#------------------------------------------------------------------------------

# Filtramos la señal

señal_filtrada = np.zeros(n)    # Inicializamos el vector de salida

k = 50                          # El orden del filtro es 2k+1 = 101
for i in range(k,n-k-1):        # Los indices no tienen que salir del rango de la señal
  señal_filtrada[i] = np.mean(señal_ruidosa[i-k:i+k])
                            
tam_ventana = 1000*(k*2+1)/fm   # Se calcula el tamaño de la ventana en milisegundos

# Reproduccion de audios (opcional)

print("\n Reproduccion de AUDIO FILTRADO (señal filtrada) ...")
sd.play(señal_filtrada,fs)       # Reproducir la señal ruidosa
status=sd.wait()

# Ploteamos el filtro, la comparacion de la señal original con la filtrada y el efecto de borde con el filtro

print("\n Graficas")

plt.subplots(1,3,figsize=(20,4))

plt.subplot(131)
plt.plot(t,señal_ruidosa,label="Señal ruidosa")
plt.plot(t,señal_filtrada,label="Señal filtrada")
plt.title(f"Filtro media movil con k={tam_ventana}-ms")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(132)
plt.plot(t,señal,"b",label="Señal original")
plt.plot(t,señal_filtrada,"r",label="Señal filtrada")
plt.title("Comparacion de señal original con la señal filtrada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(133)
plt.plot(t,señal,"b",label="Señal original")
plt.plot(t,señal_filtrada,"r",label="Señal filtrada")
plt.title(f"Efecto de borde con el filtro media movil k={tam_ventana}-ms")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.axis([0,0.5,-2,2])
plt.grid()
plt.legend()

plt.show()


