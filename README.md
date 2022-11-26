# gauss++
Gauss++ es un lenguaje imperativo de propósito general diseñado para facilitar la generación de exámenes, problemarios, libros, etc. para Olimpiada de Matemáticas. El lenguaje contiene todos los elementos básicos propios de un lenguaje además de funciones para 
 
- declarar problemas *
- generar archivos *
- seleccionar problemas *
- importar imágenes *
- imprimir expresiones matemáticas con formato *

**Pendiente de implementar*


# Manual de usuario

## Instalación 
Para poder correr un programa escrito en gauss++ es necesario instalar Python3, Lark y el presente repositorio.

Para instalar Python, visite [el siguiente link.](https://www.python.org/downloads/)

Una vez instalado Python, instale Lark con el siguiente comando en su terminal.

```bash
pip install lark
```

## Programas en Gauss++
Para correr un programa gauss++ es necesario que este sea escrito en un archivo con extensión `.gauss`. Incluya su código en la carpeta code del repositorio.

Un programa Gauss++ sigue la siguiente estructura:

- Declaración del proceso
- Declaración de las variables Gauss
- Declaración de las variables globales
- Módulos
- Problemas
- Listas de problemas
- Función genera
- Función main

Los únicos elementos obligatorios son la declaración del proceso y la función main.

La declaración del proceso es iniciada por la palabra Gauss seguida de un identificador. Es recomendado agregar un guión bajo al identificador.

A continuación se presenta un ejemplo.

#### Hello world! en gauss++
```bash
Gauss _examen
main(){
    print("Hello World!")
}
```

## Características generales de Gauss++

### Tipos primitivos
Gauss++ maneja los tipos entero (`int`), flotante (`float`), string (`string`), y booleano (`bool`).

> Las variables Gauss son variables de tipo string que serán utilizadas para la generación de los archivos.

### Variables
La declaración de variables en gauss++ sigue el siguiente formato.

```var [tipo] [nombreVariable]```

Una variable gauss++ puede empezar o no con un guión bajo, sin embargo, la primera letra siempre debe de ser una minúscula.

> La expresión regular utilizada para los identifcadores de variables es
`/[_]? [a-z]+ [a-zA-Z0-9_]*/`

Es posible declarar más de una variable en la misma línea, al igual que hacer asignaciones. Las declaraciones múltiples son delimitadas por una coma (`,`).

```bash
var int puntaje, year = 2022
var string categorias[6]
var float pesos = 60.0
var string apellido
```

#### Tipos estructurados
Gauss++ soporta tipos estructurados homogéneos de múltiples dimensiones, desde arreglos, matrices, etc. Los elementos son idexados con un límite inferior de 0. 

La sintaxis para declarar un arreglo es

```var tipo nombreArreglo [id1] [id2] ... [idn]```

```bash
var string categorias[6]
var int puntajes[5][7]
```

Cuando se declara un arreglo, sus elementos son None. En este momento, la asignación se realiza elemento por elemento.

```bash
categorias[0] = "Nivel A"
categorias[1] = "Nivel B"
categorias[2] = "Nivel C"
```

### Módulos
Gauss++ ofrece la declaración de módulos tipados y de tipo `void`. Los identificadores del módulo siguen las mismas reglas de declaración de variables referenciadas [en la sección anterior](#variables).

Es posible declarar variables locales dentro de un módulo, siempre al principio, siguiendo las reglas anteriormente mencionadas.

Las funciones tipadas necesitan tener al menos un estatuto `return` cuyo valor corresponda con el tipo de la función.

#### Parámetros 
Un módulo puede o no recibir parámetros. Su declaración es `[tipo] [nombreIdentificador]`.

```bash
int genial(int g) {
    var int e = 3
    return g * e
}

void inicia() {
    var int y, x = 1
    y = 1
    print("Estamos a punto de comenzar")
}
```

### Operadores
#### Operadores aritméticos
| Operación | Operador |
| ------------- | ------------- |
| Suma  | +  |
| Resta  | -  |
| Multiplicación  | *  |
| División  | /  |

#### Operadores lógicos
| Operación | Operador |
| ------------- | ------------- |
| Mayor qué  | >  |
| Menor qué  | <  |
| Mayor o igual qué  | >=  |
| Menor o igual qué  | <=  |
| Igual  | ==  |
| Diferente  | !=  |
| And  | and  |
| Or  | \or  |

### Estatutos
A partir de este punto, todas las variables y módulos referenciados deben de haber sido declarados previamente.
- **Asignación:**
```     
    i = 0
    arr[3] = "hola"
    x = y * 4 + 2000
```
- **Condición:**
Para condiciones, gauss++ maneja los bloques condicionales `if` y `else`. El bloque `if` puede o no ser seguido por un bloque `else`, sin embargo el bloque `else` no puede ser utilizado por sí solo.
```
if (5 < 4) {
    print(True)
} else {
    print(False)
}
```
- **Ciclo:**
En este momento, gauss++ solamente maneja el ciclo de while, siguiendo la siguiente estructura:
``` while([CONDICIÓN]) { } ```
```
i = 0
while(i<3) {
    year = 2020 + i
    i = i + 1
    print(i)
}
```

- **Escritura:**
Para escribir en la consola, se utiliza la siguiente sintaxis:

```print([TEXTO A IMPRIMIR])```

- **Lectura**
Para leer de la consola, se utiliza la siguiente sintaxis, donde el identificador debió de haber sido previamente declarado. Lo leído se almacenará en ese identificador.

```read([ID])```

- **Llamada de función:**
Para llamar una función, esta debió de haber sido declarada previamente, y se sigue la siguiente estructura:

```[id]( [param1], [param2], ... [paramn])```

```bash
hello("Garcia")
y = pelos()
print(genial(5))
```

Se deben de respetar los tipos y la cantidad de parámetros descritos en la definición de la función. Una llamada a una función puede ser utilizada por sí sola, como factor de una operación, puede ser igualada, etc. Dependiendo del tipo de retorno.


### Comentarios
Una línea de código se comenta agregando `//` al principio del comentario. Esto hará que el compilador la ignore.

```// Esto es un comentario ```

## Características propias de Gauss++
### Información general
En caso de querer utilizar las variables de gauss++, se debe de declarar la *organización*, la *etapa*, y las *categorías*, de la siguiente manera:
```bash
organizacion = "OMMCH"
etapa = "Examen Estatal"
categorias = ["Nivel A", "Nivel B", "Nivel C", "Nivel D"]
```

### Problemas
Para declarar un problema, utilice la siguiente estructura:

```bash
problema [identificador](area = [area]) {
    categoria = categorias[[indice]]
    >> [texto] | [expresion] | [import]
    ...
    opciones = [ [opcion1], [opcion2], ..., [opcionN]]
    respuesta = [respuesta]
}
```
La categoría, las opciones, y la respuesta son opcionales. 

A continuación se presenta un ejemplo.
```bash
problema problema1(area = "Teoria de Números") {
    categoria = categorias[0]
    >> "Considera cinco números de menor a mayor" 
    >> $expr("a<b<c<d<e") 
    >> ". Después de que se calculan las 10 sumas de cada pareja de números se sabe que las tres sumas más pequeñas son 32, 36 y 37, mientras que las sumas más grandes son 48 y 51. ¿Cuánto vale e?"
    opciones = [16, 17, 18, 19, "No se puede saber"]
    respuesta = 19
}
```

#### Para imprimir en el archivo
- **Imprimir texto**
Para establecer el texto que aparecerá cuando se cree el archivo, se sigue la siguiente sintaxis:

```>> [STRING]```

- **Imprimir expresiones**
Para imprimir con *formato matemático*, se sigue la siguiente sintaxis:

```>> $expr([STRING])```

- **Importar imágenes**
Para importar imágenes, se sigue la siguiente sintaxis:

```>> $import([PATH])```

### Listas de problemas 
Los problemas a incluirse se incluyen en listas, que se alimentarán a la función genera. Se incluyen los identificadores de los problemas en una lista entre corchetes. Estos deberán de haber sido previamente declarados.

```listaProblemas = [problema1, problema2, problema3]```

### Función genera
La función genera establece los datos para generar los archivos; solamenet puede ser declarada una vez. Sigue la siguiente estructura:

```bash
genera(orientacion, categoria, problemas, nombreArchivo) {
    header([STRING], [STRING], [STRING])
    titulo([STRING])
    instrucciones([STRING])
    problemasIncluidos(problemas, random = [TRUE | FALSE])
    footer([CATEGORIA])
} 
```
#### Parámetros
Los parámetros para esta función solamente son declarados como variables, obtendrán valores cuando se llame la función.
- **orientación**: "vertical" u "horizontal", determina la orientación que se desea para el archivo
- **categoría**: categoría a imprimirse en el archivo
- **problemas**: lista de problemas a incluirse en el archivo
- **nombreArchivo**: string que dará nombre al archivo a generarse

#### Funciones dentro de genera
- **header**: Establece los datos a escribirse en el header del archivo. Recibe tres parámetros de tipo string.
- **titulo**: Escribe el título del archivo; recibe un parámetro de tipo string.
- **instrucciones**: Escribe las instrucciones del archivo; recibe un parámetro.
- **problemasIncluidos**: Manipula los problemas a ser incluidos. Recibe dos parámetros: una lista, y un booleano que determina si el orden será random o no.
- **footer**: Escribe el footer del archivo; recibe un parámetro de tipo string.

Se presenta el siguiente ejemplo:

```bash
genera(orientacion, categoria, problemas, nombreArchivo) {
    header(organizacion, fecha, etapa)
    titulo("Examen Estatal")
    instrucciones("Contesta los siguientes problemas y entrega tu respuesta en una hoja separada. Tienes 50 minutos")
    problemasIncluidos(problemas, random = False)
    footer(categoria)
} 
```

### Main
La función main es la función principal del programa: la ejecución comienza aquí, y es aquí donde se realizan las llamadas a las demás funciones.

A continuación se presenta un ejemplo de cómo se llamaría la función genera.

```bash
main () {
    genera("vertical", "categorias[1]", listaProblemas, "principiantes")
}
```


## Para correr el programa
Se guarda el archivo, de preferencia en la carpeta code del repositorio, y se ejecuta el siguiente comando:

```bash
python3 gauss.py
```

Teclee el nombre de tu archivo sin el gauss, y estará ejecutando su programa gauss++. En caso de tener errores, estos aparecerán en la consola.

## Video tutorial
[Link](https://drive.google.com/file/d/11wBwxA6cnz6FIAFcPUKgP8kHdbv2heMX/view?usp=share_link) al video tutorial

## Documentación
Para conocer más, revise la documentación en el [siguiente link](https://1drv.ms/w/s!Ag7C-YtrePDRibEW6X8zUYnWT31bYw)

Link a la [propuesta](https://1drv.ms/w/s!Ag7C-YtrePDRibEOTF0NMdxTAwwxMA) del proyecto.
**pendiente a ser aprobada*

## Desarrollado por 
Nadia García A01242428
Diseño de compiladores, Semestre Agosto-Diciembre 2022