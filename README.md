<div align="center">

# FEC · Forward Error Correction

**Fundación Fulgor** · Pedro Villar · 2026

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-notebooks-F37626?logo=jupyter&logoColor=white)
![MATLAB](https://img.shields.io/badge/MATLAB-scripts-e16737?logo=mathworks&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-informes-008080?logo=latex&logoColor=white)
![Estado](https://img.shields.io/badge/curso-en%20curso-blue)

Repositorio de cursada: guías, trabajos prácticos y apuntes del curso de
Codificación para Corrección de Errores (FEC).

</div>

---

## Mapa del repositorio

```
FEC-Fulgor/
├── Trabajos Practicos/        TPs evaluables, cada uno en su propia carpeta y stack
├── Guias de Ejercicios/       guías prácticas de la cátedra, resueltas
├── Unidad 1 · 2 · 3 · 4/      material de clase y apuntes propios, por unidad
└── Bibliografia/              bibliografía de referencia del curso
```

---

## Trabajos Prácticos

| TP | Tema | Estado | Contenido |
|---|---|:---:|---|
| **TP1** | Operaciones en `GF(2^m)`: campos de Galois y polinomios | `Completo` | Librería Python propia ([`fec_algebra`](<Trabajos Practicos/Trabajo Práctico 1 - Operaciones en GF/fec_algebra>)) con clases `GF`, `GFElement`, `GFPoly`, suite de tests con `pytest` y notebook con la Guía 1 resuelta sobre la librería |

Cada TP incluye el enunciado provisto por la cátedra y, cuando corresponde, un
`README.md` propio con el detalle técnico de la solución (estructura, decisiones
de diseño, ejemplos de uso).

**TP1** → [enunciado](<Trabajos Practicos/Trabajo Práctico 1 - Operaciones en GF/TP1_FEC.pdf>) · [solución](<Trabajos Practicos/Trabajo Práctico 1 - Operaciones en GF/fec_algebra/README.md>) · [notebook](<Trabajos Practicos/Trabajo Práctico 1 - Operaciones en GF/fec_algebra/notebooks/TP2_Guia_Ejercicios.ipynb>)

---

## Guías de Ejercicios

| Guía | Tema | Estado | Enunciado | Solución |
|---|---|:---:|:---:|:---:|
| **Guía 1** | Álgebra en FEC (I) | `Completa` | [PDF](<Guias de Ejercicios/Guia1 - Algebra FEC.pdf>) | [PDF](<Guias de Ejercicios/Guia1 - VillarPedro.pdf>) |
| **Guía 2** | Álgebra en FEC (II) | `En curso` | [PDF](<Guias de Ejercicios/Guia2 - Algebra FEC.pdf>) | [LaTeX](<Guias de Ejercicios/Guia2/Guia2 - VillarPedro.tex>) (en preparación) |

La Guía 1 tiene, además, una segunda resolución integrada al TP1: ver el
[notebook de `fec_algebra`](<Trabajos Practicos/Trabajo Práctico 1 - Operaciones en GF/fec_algebra/notebooks/TP2_Guia_Ejercicios.ipynb>).

---

## Unidades del curso

| Unidad | Tema | Apunte propio | Material de cátedra |
|:---:|---|---|---|
| **1** | Introducción y motivación | [Resumen](<Unidad 1 - Introduccion/CRS-FEC-Introduccion-Resumen.md>) | [Clase 1](<Unidad 1 - Introduccion/Material de Clase/Clase_1_FEC.pdf>) · [Unidad 1](<Unidad 1 - Introduccion/Material de Clase/Unidad_1_FEC.pdf>) · [notebook](<Unidad 1 - Introduccion/Material de Clase/Unidad_1.ipynb>) · [script MATLAB](<Unidad 1 - Introduccion/Scripts Matlab/BSCExample.mlx>) |
| **2** | Códigos de control de errores (preliminares) | - | [Unidad 2](<Unidad 2 - Codigos de Control de Errores/Material de Clase/Unidad_2_FEC.pdf>) · [filmina](<Unidad 2 - Codigos de Control de Errores/Material de Clase/Filmina_2_FEC.pdf>) · [clase práctica](<Unidad 2 - Codigos de Control de Errores/Material de Clase/clasepractica1.pdf>) |
| **3** | Códigos de control de errores (continuación) | - | [Unidad 3](<Unidad 3 - Codigos de Control de Errores/Material de Clase/Unidad_3_FEC.pdf>) · [filmina](<Unidad 3 - Codigos de Control de Errores/Material de Clase/Filmina_3_FEC.pdf>) |
| **4** | Códigos de bloque importantes | - | [Unidad 4](<Unidad 4 - Codigos de Bloque importantes/Material de Clase/Unidad_4_FEC.pdf>) · [filmina](<Unidad 4 - Codigos de Bloque importantes/Material de Clase/Filmina_4_FEC.pdf>) |

---

## Bibliografía

**Lin, S. & Costello, D. J.**, *Error Control Coding* (2nd ed.). Texto de
cabecera del curso: todas las referencias teóricas de los TPs, guías y
notebooks remiten a él. [PDF](<Bibliografia/Error Control Coding - Lin, Daniel J, Costello, Jr.pdf>)
