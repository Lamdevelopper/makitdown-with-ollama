**Reporte de Resultados y Análisis de la Misión para el Concurso-Concurso Mundial de Satélites Enlatados 2026**

Matias Lamoyi[[1]](#footnote-0), Diego Valdez[[2]](#footnote-1), Axel Chàvez[[3]](#footnote-2), Adrian Thibaud[[4]](#footnote-3), Luciano Hernandez[[5]](#footnote-4), Karim Ramirez[[6]](#footnote-5) y Eythan Reyes[[7]](#footnote-6)

*Liceo Franco Mexicano AC (LFM), CDMX, 11530, México*

DR Alejando Farah[[8]](#footnote-7)

*Instituto Astronomía de la Universidad Nacional Autónoma de Mèxico (UNAM), CDMX, México*

**![](data:image/png;base64...)**

**Este documento es la plantilla para presentar el Reporte Final de Misión del proyecto desarrollado por cada equipo para el Curso-Concurso Mundial CanSat 2026. La entrega del reporte debe ser en formato PDF.**

**IMPORTANTE**

**APARTADOS A ENTREGAR PARA CUMPLIR CON ESTE PUNTO: I, II, III, APÉNDICE, AGRADECIMIENTOS Y REFERENCIAS.**

* **DESPUÉS DEL LANZAMIENTO DEL SATÉLITE ENLATADO, FALLIDO O EXITOSO, DEBERÁ VOLVER A ENVIAR ESTE REPORTE INCLUYENDO LA INFORMACIÓN SOLICITADA DEL VUELO DEL CANSAT Y LAS CONCLUSIONES, RESPETANDO ESTE MISMO FORMATO. EL REPORTE CON TODA LA INFORMACIÓN REQUERIDA SE DEBERÁ ENTREGAR EL 23 DE MAYO, DESPUÉS DE LOS LANZAMIENTOS Y ANTES DE LAS 19: 59 HORAS (HORA DE LA CIUDAD DE MÉXICO). \*OJO: PARA ESTA ENTREGA DEFINITIVA DEBERÍAN TENER TODO YA PREPARADO PARA SOLO VACIAR LOS DATOS FALTANTES SOLICITADOS Y OBTENIDOS DEL VUELO DEL SATÉLITE ENLATADO.**
* **CON LA ENTREGA DE ESTE DOCUMENTO LOS AUTORES DAN EL CONSENTIMIENTO PARA SU PUBLICACIÓN, Y DE TODO EL MATERIAL ENTREGADO EN LAS DIFERENTES ETAPAS DEL CURSO-CONCURSO MUNDIAL DE SATÉLITES ENLATADOS 2026, EN MEDIOS DIGITALES Y GRÁFICOS DE LA UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO. DICHAS PUBLICACIONES SON SIN FINES DE LUCRO.**

1. **Nomenclatura**

Incluir toda su nomenclatura de unidades y estilos en el formato del Sistema Internacional de Unidades. En esta liga pueden descargar los detalles de dicha normativa <https://www.cenam.mx/siu.aspx> .

1. **Introducción**

Este equipo presenta a continuación los elementos diseñados y manufacturados para esta misión del Mundial de CanSats 2026:

**Subsistema de Mecánica:**

Se diseñó y manufacturó el fuselaje del CanSat para asegurar la integridad estructural y supervivencia del tripulante, se diseñó sistema de autogiro y mecanismo de liberación mecánico.

**Subsistema de electrónica:**

Se diseñó sistema de captura y envío de telemetría a bordo, sistema de alimentación eléctrica, PCB (no manufacturada).

sistema de comunicación para estación terrena con doble tipo de bandas de recepción (LoRa para telemetría y wifi para foto estereoscópica con requerimientos mayores en ancho de banda).

**Subsistema de programación y control:**

Creación de algoritmos de generación de foto estereoscópica,

Protocolos de envío LoRa, Código estación terrena, algoritmos de envío y sistema de liberación de algoritmo.

1. **Descripción técnica del Satélite Enlatado**

**Telemetría:**

Sensor BMP180 y Sensor IMU MPU6050 → Datos a LilyGo Lora32 OLED → Datos a traves de protocolo Lora → → Interfaz de Usuario de la estación terranea.

![](data:image/png;base64...)

**Fotografía Estereoscópica:**

Cámaras OV5640 → ESP32-CAM → Datos via WiFi → Antena de recepción externa en la estación terranea → Interfaz de Usuario de la estación terranea.

**Despliegue Sistema de Autogiro:**

Sensor BMP180 → Detecta si altura - altura inicial < 200m → Señal a Servomotor → Servomotor con navaja corta hilo desplegando el sistema de autogiro

**Sistema de Autogiro:**

Dos palas con un área aproximadamente igual que la de un costado del CanSat para maximizar la resistencia del aire.

**Sistema de protección del Huevo:**

Esponjas directamente en contacto con el huevo, soportadas por placas de madera con resortes para amortiguación.

![](data:image/png;base64...) + ![Relleno de espuma o plástico de burbujas: ¿Cuál es más adecuado? |  Comercial Avilés](data:image/jpeg;base64...)

1. **Análisis de la información recibida por el satélite enlatado durante toda la misión**

Uno de los principales fallos y aprendizajes de esta misión fue el manejo de telemetría, al tener fallos críticos en algunos sensores, errores de conectividad y limitaciones de peso, no pudimos capturar ninguna telemetría útil.

* **Contestar de manera concisa lo solicitado en la siguiente tabla:**

| 1. Altura máxima alcanzada sobre el nivel del piso (m): | (no data) 350m\* |
| --- | --- |
| 1. Tiempo total de la misión (s): | (no data) |
| 1. ¿Se desplegó el sistema de autogiro y ayudó al descenso controlado del CanSat? | Si, sin embargo el sistema de autogiro no logró estabilizar ni frenar la caída del CanSat Correctamente |
| 1. En caso afirmativo de la pregunta 3: ¿a qué altitud en metros se desplegó el autogiro sobre el nivel del suelo? | 350m \* |
| 1. Velocidad máxima alcanzada después de la liberación y antes del despliegue del autogiro (m/s): | No Data |
| 1. Velocidad mínima alcanzada después de la liberación y después del despliegue del autogiro (m/s): | No Data |
| 1. Aceleración máxima y mínima alcanzada durante toda la misión (m/s2): | No Data |
| 1. ¿Sobrevivió el astronauta (huevo de gallina)? Contestar con SÍ o NO. | NO |
| 1. Número total de paquetes de datos recibidos durante toda la prueba: | 0 |
| 1. ¿Logró transmitir los 30 segundos después del aterrizaje? (SI o NO): | NO |

1. **Misión estereoscópica**![](data:image/png;base64...)

* **Incluir el resultado de la imagen (o imágenes) estereoscópicas obtenidas durante la misión. Realiza un análisis técnico del resultado.**

No se logró capturar ni enviar foto estereoscópica.

1. **Desempeño durante toda la misión**

Deben incluir de manera clara y concisa únicamente lo solicitado acerca de la información recibida por la estación terrena proveniente del satélite enlatado.

Incluir la información desde el momento en que inicia la elevación y hasta el final de la misión (30 segundos después del aterrizaje).

En función de los datos recopilados durante toda la misión del satélite enlatado, presentar las siguientes gráficas:

1. Altura (m) vs Tiempo (s)

N/A

1. Altura (m) vs Presión (Pa)

N/A

1. Altura (m) vs Velocidad (m/s).

N/A

1. Altura (m) vs Aceleración (m/s2)

N/A

1. Tiempo (s) vs Número de paquetes transmitidos por el CanSat de forma acumulativa.

N/A

1. **Conclusiones**

**Describir sintéticamente las conclusiones de la misión ejecutada de acuerdo a los resultados alcanzados, el nivel de éxito alcanzado en toda la misión, así como las posibles mejoras que se podrían realizar al diseño del satélite enlatado y al trabajo de gestión implementado por el equipo.**

Los resultados alcanzados en la misión no fueron los esperados, esto fue causado por una falla en el sistema de electrónica y telecomunicaciones que nos dejaron sin telemetría válida e inhabilitaron el control abordo junto con el sistema de despliegue de autogiro, aunado a esto, nuestro CanSat fue muy pesado. Aún así, nuestra estructura logró resistir perfectamente al impacto.

Nuestro tripulante no sobrevivió, aprendimos que fue causado principalmente por unas esponjas de cocina de polietileno muy suaves, no tener el huevo envuelto en papel espuma y estar protegidos por los cheetos de embalaje tal como se planeó en el CDR (esto porque nuestro impacto fue lateral, dónde el huevo estaba menos amortiguado).

Otro punto clave que aprendimos y vamos a tomar en cuenta para la siguiente edición es hacer el rediseño de nuestro interior, para lograr una estructura más ligera, y optimizar la disposición de componentes con una PCB.

Otro punto a tomar en cuenta es la gestión del sistema eléctrico, ya que nuestra distribución y envío de energía a sensores no fueron lo más óptimo, nuestra batería tenía un solo step-down el cual tenía una sola salida USB tipo A, esta singular salida más unos separadores no permitieron el adecuado energizado de los ESP’s a bordo y mucho menos los sensores, antes de tan siquiera ejecutar el código.

La gestión de equipos resultó exitosa, con la excepción de algunos integrantes retrasando en sus partes o no logrando los resultados deseados por falta de compromiso en el proyecto. Hay que tomar en consideración que solo teníamos una hora semanal en equipo a la semana, cada miércoles en el Club aeroespacial, vamos a mejorar eso para la siguiente edición y tener los sistemas integrados con mayor antelación.

El reto principal superado fue la estructura, ya que logró sostenerse excepcionalmente después del impacto, pese a ser completamente de madera sin uniones por tornillos.

**Mencionar los puntos que consideren más significativos sobre su experiencia en el Curso-Concurso Mundial de Satélites Enlatados 2026.**

1. El aprendizaje en mecánica y electrónica para hacer un CanSat
2. Superar retos y coordinación en equipo
3. Conocer gente de otros equipos, ver que teníamos soluciones similares y recibir feedback para mejorar en la próxima edición
4. Aprender a redactar documentos técnicos y sentir la emoción de ver tus planos y meses de trabajo subidos al drone.
5. Aprender a solucionar problemas en el momento con recursos limitados y trabajar bajo presión

**Recomendaciones para los organizadores del concurso.**

Consideramos que la organización de la competencia fue llevada a cabo de manera muy profesional, nos hubiera gustado tener feedback al final de cada entrega de documentos, pero entendemos que se complica al tener muchos equipos compitiendo y no necesariamente es posible.

Durante el evento todo estuvo perfecto desde nuestro punto de vista.

**Apéndice**

Si requieren añadir apéndices con información adicional, hacerlo antes de la sección de agradecimientos.

**Agradecimientos**

Si desea agregar agradecimientos, incluirlos antes de las referencias.

Queremos dar nuestros agradecimientos especiales al Comité Organizador de la competencia por dejarnos participar incluso siendo estudiantes de Preparatoria,

Agradecemos la participación del comité corrector que nos ayudó a aprender a hacer reportes técnicos escritos de forma profesional,

Agradecer igualmente a todo el equipo del Programa Espacial Universitario presente apoyando en todos los aspectos y dando lugar a un evento increíble y que recordaremos con mucho cariño

Queremos agradecer a nuestro asesor académico el Doctor Alejandro Farah por todo su apoyo y el tiempo que nos dedicó y su gran disposición de ayudar

Agradecemos también a todos los equipos que participaron por mostrarse siempre solidarios, crear un gran ambiente y por tener siempre voluntad de apoyar incondicionalmente con consejos, apoyo moral y material prestado.

**Referencias**

Incluir las referencias más significativas utilizadas en el desarrollo de su satélite.

<http://airfoiltools.com/search/index>

Guía de misión del Programa Espacial Universitario, y contenido en youtube

Github

Unit electrónica

1. 4to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-0)
2. 4to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-1)
3. 4to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-2)
4. 4to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-3)
5. 4to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-4)
6. 2do Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-5)
7. 6to Semestre Preparatoria, Liceo Franco Mexicano AC, Ciudad De México, 11530, México. [↑](#footnote-ref-6)
8. Técnico Académico Titular C, Instituto Astronomía de la UNAM. [↑](#footnote-ref-7)