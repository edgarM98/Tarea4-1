#########################################
#########################################
#####                               #####
#####    Maria Paula Ruiz Segura    ##### 
#####             B76878            #####
#####                               #####
#####            Tarea 4            #####
#####                               #####
#####            Grupo 2            #####
#####                               #####
#########################################
#########################################

# Paquetes que serán de utilidad. 
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt


#Se importa el paquete 'pandas' para poder agregar los datos al programa y
#luego se lee el archivo
import pandas as pd
bits2 = pd.read_csv('bits10k.csv', header=None)
bits = np.array(bits2)

# Número de bits
N = 10000 

### PARTE 1, crear un esquema de modulación BPSK para los bits presentados. ###

# Frecuencia de operación
f = 5000 # Hz

# Duración del período de cada símbolo (onda)
T = 1/f # 0.2 ms

# Número de puntos de muestreo por período
pts = 50

# Puntos de muestreo para cada período
Tpts = np.linspace(0, T, pts)

# Creación de la forma de onda de la portadora
sen = np.sin(2*np.pi * f * Tpts)

# Visualización de la forma de onda de la portadora
plt.figure(0)
plt.plot(Tpts, sen)
plt.xlabel('Tiempo / s')

# Frecuencia de muestreo
fs = pts/T 

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*pts)

# Inicializar el vector de la señal modulada Tx
senal = np.zeros(t.shape)

# Creación de la señal modulada BPSK
for k, b in enumerate(bits):
    if b == 1:
        senal[k*pts:(k+1)*pts] = sen
    else: 
        senal[k*pts:(k+1)*pts] = -sen

# Visualización de los primeros bits modulados
pb1 = 0
pb2 = 10
plt.figure(1)
plt.plot(senal[pb1*pts:pb2*pts])
plt.xlabel('Tiempo / s')

### PARTE 2, calcular la potencia promedio de la señal modulada generada ###
# Se usan fórmulas conocidad para la potencia y la potencia instantánea de una señal 

# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)

print('La potencia promedio es: ', Ps, 'W. \n')

## PARTE 3, Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco ##
## gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB. ###

# Relación señal-a-ruido deseada
SNRt = [-2, -1, 0, 1, 2, 3] # Valores de SNR

BER = np.zeros(6)

for i in range(6):  
    SNR = SNRt[i]
    
    # Potencia del ruido (Pn) para SNR y potencia de la señal (Ps) dadas
    Pn = Ps / (10**(SNR / 10))

    # Desviación estándar del ruido
    sigma = np.sqrt(Pn)

    # Crear ruido (Pn = sigma^2)
    ruido = np.random.normal(0, sigma, senal.shape)
    
    # Simular "el canal": señal recibida
    Rx = senal + ruido
    
    # Visualización de los primeros bits recibidos
    pb = 10
    plt.figure(2)
    plt.plot(Rx[0:pb*pts])
    plt.xlabel('Tiempo / s')

    ## PARTE 4, Graficar la densidad espectral de potencia de la señal con el ### 
    ## método de Welch (SciPy), antes y después del canal ruidoso. ##############

    # Antes del canal ruidoso
    fw, PSD = signal.welch(senal, fs, nperseg=1024)
    plt.figure(3)
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    
    # Después del canal ruidoso
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure(4)
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz') 

    ## PARTE 5, Demodular y decodificar la señal y hacer un conteo de la tasa ###
    ## de error de bits (BER, bit error rate) para cada nivel SNR. ##############
    
    # Pseudo-energía de la onda original 
    Es = np.sum(sen**2)
    
    # Inicialización del vector de bits recibidos
    bitsRx = np.zeros(bits.shape)
    
    for k, b in enumerate(bits):
        Ep = np.sum(Rx[k*pts:(k+1)*pts] * sen)
        if Ep > Es/2:
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0
        
    err = np.sum(np.abs(bits - bitsRx))
    BER[i] = err/N
    
    print('Cuando SNR es: ', SNR, 'el ruido es: ', BER[i])

## PARTE 6, Graficar BER versus SNR ## 

plt.figure(5)
plt.plot(BER, SNRt)
plt.xlabel('BER (bit rate error)')
plt.ylabel('SNR / dB') 

