### PT-BR: Primeiramente você deve ter o python instalado.
###### EN: First, you must have Python installed.

##### ALERTA: O PROJETO USA A BIBLIOTECA WINSOUND PARA MANIPULAR OS SONS, O QUE PODE CAUSAR CONFLITOS COM O LINUX
###### ALERT: THE PROJECT USES THE WINSOUND LIBRARY TO HANDLE SOUNDS, WHICH MAY CAUSE CONFLICTS WITH LINUX.

[Click here to download python](https://www.python.org/downloads/)  
Por compatibilidade, recomenda-se as versões 3.8 ou no máximo 3.10.  
For compatibility, versions 3.8 or up to 3.10 are recommended.

### Após baixar o python  
###### After downloading python

Crie uma pasta onde colocará os arquivos e, acessando essa pasta pelo terminal, crie seu ambiente de execução e o ative.  
Create a folder where you will place your files, and by accessing this folder through the terminal, create your execution environment and active it.

~~~python
python3 -m venv .venv

# for linux
source .venv/bin/activate

# for windows
.\.venv\Scripts\activate
~~~

Instale as bibliotecas  
Install the librarys

Bibliotecas | 
---------   | 
Mediapipe   |
OpenCV      |
Winsound    |
OS          |
Json        |
Tkinter     |

##### OBS: Tkinter, Json, OS e Winsound(para windows) são bibliotecas padrões do python, logo não necessitam serem instaladas.  
###### NOTE: Tkinter, Json, OS, and Winsound (for Windows) are standard Python libraries, so they do not need to be installed.

~~~bash
pip install mediapipe
pip install opencv-python
~~~

Esses são os passos cruciais.  
These are the crucial steps.
