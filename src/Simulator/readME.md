# Simulador

# Description
Este proyecto busca desarrollar una plataforma de simulacion para los robots otto conectados al server

# Instalation
 - Instalar todos los paquetes con pip install -r requirements.txt en el root del proyecto
 - La clase a ser utilizada como client se encuentra en lib/client
 - La funcion para generar los qr (Position, text, size) a partir de la imagen se encuentra en lib/qrReader

 # Getting Started 
 - Generar un condigo QR (pueden usar esta web https://www.the-qrcode-generator.com/) de tal forma que el texto almacenado sea un mail identificatorio 
 - Imprimir el codigo QR y pegarlo en la parte superior del robot 
 

 # Test Enviroment 
 - Utilizar una webcam o en su ausencia un telefono transmitiendo mediante wifi
    - https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US
    - https://m.apkpure.com/vxg-rtsp-server-ip-camera/veg.mediacapture.sdk.test.server
    - Obtener la `url` proveida por la app 

 - Conectar la camera cv2.VideoCapture(0||`url`)
 - Ubicar la camera en la parte superior en un soporte fijo de tal manera que pueda visualizar al robot y el plano focal e la camera sea lo mas paralelo posible al plano donde se ubicara el qr 
 - Montar una region cuadrada de la siguiente manera (El gato debe ser estandarizado)

    ![Image not Found](https://www.womansworld.com/wp-content/uploads/2019/01/cats-in-squares.jpg)
    - El cuadrado debe ser construido de tal manera que el ancho de la impresion del codigo QR sea al menos 1/6 de uno de sus lados 
 - Dentro del cuadrado establecer un origen (Alguna de las esquinas) 
 - Ubicar la camara de tal forma que la imagen percibida contenga la mayor parte posible del cuadrado dibujado (Caso ideal: {La imagen percibida es un rectangulo azul con sus bordes en los bordes de la imagen})
 - Ubicar el codigo QR en la imagen y utilizar la funcion `getQRS` de lib/qrReader con la imagen capturada por la camara verificando que detecte el codigo 
 - Retirar al gato 

 # Code

 - Position

    - Crear una funcion `getPosNorm(img)` en python de tal forma que a partir de los datos proveidos por la funcion anterior permita general el centro de la posicion del QR `(Cx,Cy)`, las dimensiones de la card `(wc,hc)` , el texto y las dimensiones de la imagen `[W,H]` 
    - Normalizar la posicion   `[xn,yn]=[Cx/W,Cy/H]`
    - Normalizar las dimensiones `[wn,hn]=[wc/W,hc/H]`
    - Construir el dict `{x:xn,y:yn,w:wn,h:hn}` y retornarlo como salida de la funcion 
    - Crear un fork del repo actual y guardar el script anterior en su fork bajo el path `Simulator/posNorm.py`
    - Testear la funcion 
    - Obtener una foto de la imagen capturada por la camera superior y subirla a `Simulator/camera.png`
    - Screen de la pantalla imprimiendo el output de la funcion y el frame capturado con cv2.imshow y subirlo a `Simulator/screen.png`

- Completar el siguiente sheet con mail  https://docs.google.com/spreadsheets/d/1i-rm3hZDKwqlCrBOrCRxgDBqB0jtZm0hU4ir3Lu2l48/edit?usp=sharing
- Due Date: 07/05/20






