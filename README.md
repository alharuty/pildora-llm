# Cómo desplegar un LLM en [replicate.com](https://replicate.com/) paso a paso

## ¿Qué son las LLMs?

Las LLMs (Large Language Models o Modelos de Lenguaje de Gran Tamaño) son sistemas de inteligencia artificial entrenados con enormes cantidades de texto para comprender y generar lenguaje humano de manera natural. Estos modelos, como GPT (Generative Pre-trained Transformer), pueden realizar tareas como responder preguntas, redactar textos, traducir idiomas o resumir información. Funcionan prediciendo la siguiente palabra en una oración según el contexto, lo que les permite mantener conversaciones coherentes y realizar tareas complejas relacionadas con el lenguaje.

## ¿Qué es un despliegue?

El despliegue (deployment) en machine learning o desarrollo de software es el proceso de llevar un modelo o aplicación desde un entorno de desarrollo a un entorno de producción, donde puede ser utilizado por usuarios reales. Implica preparar el sistema para que sea accesible, escalable y estable, ya sea a través de una API, una aplicación web o un servicio en la nube. Es un paso crucial para poner en práctica los modelos entrenados y permitir su uso en el mundo real.

## ¿Qué es replicate.com?

Replicate.com es una plataforma que permite a desarrolladores y empresas ejecutar modelos de inteligencia artificial en la nube sin necesidad de configurar servidores ni preocuparse por la infraestructura. Ofrece una amplia variedad de modelos ya entrenados, como modelos de texto, imagen o audio, que se pueden utilizar a través de simples llamadas a una API. Es especialmente útil para integrar modelos de machine learning en proyectos de forma rápida y sencilla.


En este ejercicio vamos a descrubrir todo el flujo de trabajo que se necesita para desplegar nuestro LLM a replicate.com.

Para ello he creado un archivo predict.py que utiliza el modelo `tiiuae/falcon-rw-1b` de [HuggingFace.](https://huggingface.co/tiiuae/falcon-rw-1b) Este modelo es gratuito, rápido, requiere poco RAM, compatible con transformers, y a diferencia de otros modelos como pueden ser "mistral-7B-Instruct-v01" que dependen de token de acceso personal (PAT) este modelo es de libre uso.

Para poder desplegar nuestro modelo primero debemos crear una cuenta tanto en [HuggingFace.co](https://huggingface.co/) como en [replicate.com](https://replicate.com/) y crear nuestras variables de entorno y tenerlos presentes para poder usar el CLI de nuestro terminal:

### 1. Variables de entorno (.env)

- `HUGGINGFACE_HUB_TOKEN`
- `replicate CLI auth Token`

### 2. El esquema de carpetas necesaria es la siguiente:

    modelo_llm/
    ├── .env
    ├── predict.py              # setup del modelo
    ├── requirements.txt        # 

1. Crea y activa el entorno virtual `python3 -m venv .venv && source .venv/bin/activate`
2. Instala las dependencias: `pip install -r requirements.txt`

### 3. requirements.txt más importantes para el despligue

`pip install torch`

`pip install transformers`

`pip install accelerate`    # importante oara el device_amap="auto"

`pip install cog`           # herramienta oficial de replicate para empaquetar modelos en Docker y subirlos

`pip install replicate`


### 4. Autentica HuggingFace para poder usar el modelo

1. `huggingface-cli login`
2. Pega en el terminal tu token personal
3. Add token as git credential? y

### 5. Crea el modelo en [replicate.com](https://replicate.com/create)

Models > Create new model > Create

### 6. Instala Cog

- `sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)`
- Ingresa la clave de tu ordenador
- `sudo chmod +x /usr/local/bin/cog`

### 7. Inicializa Cog en tu proyecto

- `cog init`

> [!NOTE]
>
> Este comando creará los archivos cog.yaml y predict.py (archivo que ya teníamos creado y nombrado con nuestro modelo)

### 8. Edita cog.yaml en caso necesario

```
build:
  python_version: "3.13"
  python_requirements: requirements.txt

predict: "predict.py:Predictor"
```

### 9. Ejecuta cog

`cog build`

> [!NOTE]
>
> Te tiene que imprimir en el terminal "Image build as cog-nombre-modelo"

### 10. Prueba localmente con Cog

`cog predict -i pregunta="Dime un producto de limpieza que blanquee la ropa"`

> [!NOTE]
>
> Esto debería devolverte en el terminal la respuesta del modelo, y eso significa que el modelo funciona correctamente y está listo para desplegar.

### 11. Sube la imagen a replicate

1. `cog login`
2. Presiona Enter en el terminal
3. Pega el CLI Token de tu cuenta de replicate
4. `cog push r8.im/tu-usuario/nombre-modelo`

### 12. Prueba el modelo en la web o desde la API

Una vez subido, verás una URL como: https://replicate.com/tu-usuario/nombre-modelo


Desde ahí podrás:
- Probar el modelo con inputs reales
- Compartir la demo con otros
- Obtener el endpoint de la API REST

También puedes hacer llamadas desde Python:

```python
import replicate

output = replicate.run(
    "tu-usuario/nombre-modelo:version",
    input={"pregunta": "Dime un producto de limpieza que blanquee la ropa"}
)
print(output)
```
