---
fecha: 2026-07-07
fuente: 
tags: cursos/FEC
---
# Clase 1: Introducción al curso de FEC

## 1. El problema: transmitir información de forma confiable

Hoy la información se transmite y almacena en forma digital. La cadena es: **fuente + codificador de fuente** (= fuente digital) → **modulador → canal físico → demodulador** (= canal digital) → decodificador de fuente. El demodulador recupera bits de una señal corrompida por el canal, y cuando la tasa de errores es alta, la calidad se degrada.

**La idea central es la redundancia**, inspirada en los lenguajes naturales: si leés "caza" en lugar de "casa", reconocés la palabra correcta porque la mayoría de las combinaciones de letras no son válidas. El **codificador de canal** introduce redundancia estructurada; el **decodificador de canal** depura la salida del demodulador.

## 2. El canal y el ruido

- **Canal AWGN**: ruido aditivo gaussiano. Con BPSK (1 bit por símbolo) y detección coherente óptima, la probabilidad de error de bit sin codificar es $p = Q(\sqrt{2E_s/N_0})$. La calidad del canal se mide con $E_b/N_0$. Cota útil: $Q(x) \le \frac{1}{2}e^{-x^2/2}$.
- **BSC (canal binario simétrico)**: es el AWGN cuantizado a dos niveles (decisión dura). Queda descrito por una única probabilidad de transición $p$.
- **Decisión suave y borrados**: si el demodulador entrega un valor real que indica su confianza, hablamos de _soft decision_ (mejor desempeño que la decisión dura). Un _borrado_ (erasure) es un símbolo marcado como poco fiable: se conoce su posición pero no su valor.
- **Tipos de errores**: aleatorios (BSC, AWGN sin memoria) vs. **en ráfaga** (rayón en un disco, desvanecimiento en radio — canales con memoria, modelados con estados). Los canales compuestos combinan ambos.

## 3. Redundancia y tipos de códigos

- **Códigos de bloque (n, k)**: k bits de mensaje → palabra de código de n > k bits, sin memoria. Redundancia $r = n-k$, tasa $R = k/n \le 1$.
- **Códigos continuos (convolucionales)**: toman $k_0$ bits y generan $n_0 > k_0$, pero cada salida depende también de $M$ bloques anteriores (memoria). Longitud de restricción $K = M+1$. Los decodificadores continuos se llevan mejor con decisión suave; los de bloque manejan bien los borrados. Suelen combinarse mediante **concatenación**.

**Ejemplos simples**: repetición (3,1) con $d_{min}=3$ corrige 1 error; paridad simple $(k+1, k)$ con $d_{min}=2$ solo detecta; códigos en arreglo (paridad por fila y columna) localizan y corrigen 1 error, base de los códigos producto.

**Distancia mínima**: $d_{min}$ gobierna la capacidad del código, detecta hasta $d_{min}-1$ errores, corrige hasta $t = \lfloor(d_{min}-1)/2\rfloor$.

**Intercalado (interleaving)**: reordena símbolos de varias palabras antes de transmitir; una ráfaga concentrada se transforma, al des-intercalar, en pocos errores por palabra. *Clave en el estándar 400ZR del TP final.*

## 4. FEC vs. ARQ

- **FEC**: canal unidireccional; el receptor corrige solo, sin retransmisión. Ejemplos: almacenamiento digital, espacio profundo (encoder simple a bordo, decoder complejo en Tierra). **Es el foco del curso**.
- **ARQ**: canal bidireccional; se solicita retransmisión al detectar errores. Variantes: stop-and-wait, go-back-N, selective repeat. Los híbridos FEC+ARQ se ven al final del curso.

## 5. El marco de Shannon (1948)

- **Entropía**: $H(p) = -p\log_2 p - (1-p)\log_2(1-p)$; máxima (1 bit) en $p=0{,}5$, nula si $p=0$ o $1$. Es el mínimo de bits necesarios para representar la fuente.
- **Capacidad de canal**: para AWGN limitado en banda, $C = B\log_2(1+S/N)$ (crece linealmente con B, solo logarítmicamente con la potencia). Para el BSC: $C = 1 - H(p)$.
- **Teorema de codificación de canal**: para toda tasa $R < C$ existen códigos con probabilidad de error arbitrariamente pequeña (decae exponencialmente con n). **Es existencial, no constructivo**: no dice cómo encontrar ni decodificar esos códigos. Cerrar esa brecha es el contenido del resto del curso.
- **Decodificación MLD**: elegir la palabra $v$ que maximiza $P(r|v)$. Sobre el BSC equivale a mínima distancia de Hamming.
- **Límite de Shannon**: $E_b/N_0$ mínimo para comunicación confiable a tasa R. Para BPSK sobre AWGN: 0,187 dB con $R=1/2$; el límite absoluto ($R \to 0$) es −1,6 dB.

## 6. Ganancia de codificación: ejemplo numérico clave

Para BER objetivo $10^{-5}$:

- BPSK sin codificar: 9,65 dB (referencia)
- Límite de Shannon (R=1/2): 0,188 dB → ganancia máxima ≈ **9,46 dB**
- Código convolucional real (R=1/2, m=6, decisión suave): 4,15 dB → ganancia de **5,35 dB**, todavía a 3,96 dB del límite.

Conclusión: codificar conviene mucho, pero queda una brecha con el límite teórico. Cerrarla con códigos más largos y potentes es la historia del resto del curso.

## 7. Panorama del curso

Familias vistas como aproximaciones sucesivas al límite de Shannon: códigos de bloque lineales (G/H, síndrome, dmin) → Hamming, Reed–Muller, Golay, producto → cíclicos (polinomios, registros de desplazamiento) → BCH y Reed–Solomon (cuerpos de Galois) → convolucionales y Viterbi → **Turbo y LDPC** (a décimas de dB del límite). Cierre: aplicaciones reales (almacenamiento, DVB, espacio profundo, 4G/5G, Wi-Fi) e implementación colaborativa de un FEC completo basado en **OIF-400ZR**, donde reaparecen concatenación, intercalado y decisión suave.
