# Tarea4
## Modelos probabilísticos de señales y sistemas
## María Paula Ruiz Segura, B76878

- **(20 %) Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.**

  Para crear el esquema de modulación BPSK se inicia leyendo la lista de 10000 bits brindada. Se asigna una frecuencia de operación de 5000 Hz, como se solicita, lo cual produce un período de 0.2 ms. Se definen además 50 puntos de muestreo para cada período. Tomando en cuenta estas consideraciones, se genera una forma de onda sinusoidal normalizada para transmitir los bits. Al hacer el plot de esta figura se obtiene: 
  
   ![enter image description here](/onda.png)
  
  Con esta forma de onda, ahora solo se necesita realizar la modulación BPSK. Aquí se crea la variable *senal* para almacenar los datos de la señal modulada. Esta modulación se realizó con el siguiente fragmento de código: 
  
      # Creación de la señal modulada BPSK
      for k, b in enumerate(bits):
        if b == 1:
            senal[k*pts:(k+1)*pts] = sen
        else: 
            senal[k*pts:(k+1)*pts] = -sen
            
  Donde *pts* es la variable que contiene el número de puntos de muestreo por período y *sen* es la variable que contiene la forma de onda sinusoidal. Con esta modulación, se obuvo la gráfica para los primeros 10 bits de la lista, se usa una muestra de la lista como esta pues el graficar la modulación de los 10 000 bits no sería de mucha utilidad puesto que son muchos y en la gráfica no se apreciaría el comportamiento, asique solo se grafica la modulación de una fracción pequeña de los bits para confirmar la correcta modulación. La gráfica obtenida es la siguiente: 
  
  ![enter image description here](/ModulaciónBPSK.png)
  
  Con la gráfica es posible confirmar la validez de la modulación BPSK obtenida, puesto que se observa claramente los cambios en la onda sinusoidal cuando hay un cambio en los bits. Es decir, si en la cadena de bits hay una serie de ceros (0, 0, 0), en la modulación que se obtendrá se va a observar la gráfica sinusoidal (*sen*), pero si hay un cambio (como en 0, 0, 1) se va a observar un cambio en la fase en la forma de onda (*-sen*). Este comportamiento es justamente el obtenido. 
  
- **(10 %) Calcular la potencia promedio de la señal modulada generada.**

  Para obtener la potencia promedio se obtiene primero la potencia instantánea de la señal modulada, esta potencia instantánea se obtiene elevando la señal al cuadrado. Luego para obtener la potencia promedio deseada se integra la potencia instantánea y se divide entre el número de total de bits multiplicado por el período. El resultado obtenido fue:

  <p align="center">
    <img src="https://render.githubusercontent.com/render/math?math=Pprom = 0.4900009 W">  
  </p>

- **(20 %) Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.**

  Para simular el canal de ruido blanco gaussiano, se crea inicialmente una lista con los seis posibles valores para SNR (-2, -1, 0, 1, 2, 3). El ruido se crea usando *numpy.random.normal* la cual crea muestras aleatorias en una distribución normal. La media elegida para esto fue 0, la desviación estándar adecuada fue calculada por medio de la raíz cuadrada de la potencia del ruido, la cual a su vez fue calculada dividiendo la potencia de la señal entre 10 elevado al valor SNR entre 10. El tamaño de estos datos en distribución normal es el mismo tamaño que la señal. Finalmente, este ruido se sumaba a la señal original para generar la señal ruidosa que simula el canal ruidoso, esto se muestra en las siguientes líneas de código:

      # Crear ruido (Pn = sigma^2)
      ruido = np.random.normal(0, sigma, senal.shape)

      # Simular "el canal": señal recibida
      Rx = senal + ruido
    
  Al graficar esta señal ruidosa para un SNR de -2 se obtiene la siguiente gráfica:
 
   ![enter image description here](/Ruido.png)
 
  Las señales ruidosas obtenidas para todos los seis valores necesarios de SNR se muestra en la siguiente grafica: 
 
  ![enter image description here](/RuidoTodas.png)
 
 - **(10 %) Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.**
  Para graficar la densidad espectral de potencia antes del ruido se usaron las siguientes líneas de código: 
 
          # Antes del canal ruidoso
          fw, PSD = signal.welch(senal, fs, nperseg=1024)
          plt.figure()
          plt.semilogy(fw, PSD)
    
 Para esta densidad espectral se obtuvo la misma gráfica para todos los valores de SNR, esto es de esperar pues esto es antes del ruido, por lo que no se debe ver afectada por    este. La gráfica obtenida es la siguiente: 
 
 ![enter image description here](/DensidadAntes.png)
 
  Para graficar la densidad espectral de potencia después del ruido se usaron las siguientes líneas de código: 
 
      # Después del canal ruidoso
      fw, PSD = signal.welch(Rx, fs, nperseg=1024)
      plt.figure()
      plt.semilogy(fw, PSD)
 
 Para esta gráfica se puede observar cómo para diferentes valores de SNR el comportamiento es el mismo, sin embargo hay una variación en la magnitud de la densidad espectral.  Esto se observa en la siguiente gráfica, donde la línea azul es la densidad cuando SNR = -2, la línea anaranjada cuando SNR = -1 y así sucesivamente: 
 
 ![enter image description here](/DensidadDespues.png)
 
 - **(20 %) Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.**
 
  Para demodular y decodificar la señal debe ser posible detectar en la señal ruidosa el comportamiento de la señal original. Para esto se cálculo la energía en la señal original y luego la energía en la señal ruidosa. Si la energía en la señal ruidosa es por lo menos la mitad de la energía en la señal original, se puede decir que en la señal original había un 1, si la energía de la señal ruidosa es menor se dice que en la señal original había un 0. Fue posible confirmar la utilidad de este procedimiento pues la lista de bits obtenida luego de este proceso de demodulación coincide con la lista de bits original. Esto se realizó en las siguientes líneas de código: 
  
    for k, b in enumerate(bits):
          Ep = np.sum(Rx[k*pts:(k+1)*pts] * sen)
          if Ep > Es/2:
              bitsRx[k] = 1
          else:
              bitsRx[k] = 0
  
  La tasa de error de bits obtenida para cada valor de SNR es: 
  
| SNR | Ruido |
|:-:|:-:|
| SNR = -2 | 0.0013 |
| SNR = -1 | 0.0007 |
| SNR = 0 | 0.0 |
| SNR = 1 | 0.0 |
| SNR = 2 | 0.0 |
| SNR = 3 | 0.0 |

Como se observa, conforme aumenta el valor de SNR, la tasa de error disminuye hasta ser inexistente. 
Esta prueba se puede realizar con otros valores de SNR con los cuáles se pueda visualizar mejor la relación, como con valores de SNR de -5 a 0 dB.
La tasa de error de bits obtenida para estos valores de SNR es: 

| SNR | Ruido |
|:-:|:-:|
| SNR = -5 | 0.0116 |
| SNR = -4 | 0.0072 |
| SNR = -3 | 0.0027 |
| SNR = -2 | 0.0016 |
| SNR = -1 | 0.0003 |
| SNR = 0 | 0.0 |

Como se observa, para estos valores de SNR se obtuvieron valores más claros de tasa de error, sin embargo el comportamiento sigue siendo el mismo: conforme aumenta el valor de SNR disminuye la tasa de error. 

- **(20 %) Graficar BER versus SNR.**
La gráfica obtenida cuando se usan valores de SNR entre -2 y 3 dB es: 

![enter image description here](/BERvsSNR_2a3.png)

La gráfica obtenida cuando se usan valores de SNR entre -5 y 0 dB es: 

![enter image description here](/BERvsSNR_5a0.png)

Cabe descatacar que los valores obtenidos para la tasa de error de bits (BER) y por consiguiente estas gráficas, pueden variar de acuerdo a cada simulación, puesto que dependen del comportamiento que tenga el ruido y este se está creando de forma aleatoria cada vez que se corre el programa. 
 
 



