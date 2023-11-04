from django.db import models
from django.contrib.auth.models import User
import ultralytics
import os
import cv2
from langchain.llms import Replicate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

object_detector = ultralytics.YOLO('core/models/best.pt')

os.environ["REPLICATE_API_TOKEN"] = "r8_Vjc3lXrrj0wXA8KMEKb9L3UHYaHXXvB229IQ1"

llm = Replicate(
    model="meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    model_kwargs={"temperature": 0.75, "max_length": 500, "top_p": 1},
)

prompt = PromptTemplate(input_variables=["coordinates"],
                        template=""" I would give you data from a object detection algorithm with object class and coordinates and you should,
make a detalied guess of what's happening on the image (Is an aerial image taken from a drone):

Example:
"The image show many cows over the field during the day, cars are traveling over a near highway"

Data:
{coordinates}

Image Description:


""")



class Drone(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    modelo = models.CharField(max_length=50)
    autonomia = models.PositiveIntegerField()  # Autonomía de vuelo en minutos
    velocidad_maxima = models.PositiveIntegerField()  # Velocidad máxima en km/h
    carga_maxima = models.PositiveIntegerField()  # Carga máxima en gramos
    disponibilidad = models.BooleanField(default=True)
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2)
    fotografia=models.ImageField(upload_to='images/drones',null=True)

    def __str__(self):
        return self.nombre

class Log(models.Model):
    
        drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
        user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
        timestep = models.DateTimeField(auto_now_add=True)
        fotografia = models.ImageField(upload_to="images/drones", null=True)
        fotografia_boxes = models.ImageField(upload_to="images/drones", default="images/drones/null.jpg")
        description = models.TextField(null=True, blank=True)


        class Meta:
            verbose_name = "Log "
            verbose_name_plural = "Logs"

        def save(self, *args, **kwargs):
            super(Log, self).save(*args, **kwargs)
            if self.fotografia:

                results = object_detector.predict(self.fotografia.path)

                image = cv2.imread(self.fotografia.path)

                image_string = ""
                for r in results:
                    for clf, box in zip(r.boxes.cls, r.boxes.xyxy):
                        box = box.cpu().numpy().astype(int)
                        cv2.rectangle(image, (box[0],box[1]),(box[2],box[3]), color=(0, 0, 255), thickness=2)
                        cv2.putText(image,r.names[int(clf)] , (box[2] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        image_string += "Found " + r.names[int(clf)] + " at cordinates " + str(box)

                cv2.imwrite("images/drones/" +  str(self.timestep) + "boxes.jpg", image)
                text = llm(prompt.format(coordinates=image_string))
                print(text)
                self.description = text

                self.fotografia_boxes = "images/drones/" +  str(self.timestep) + "boxes.jpg"

            super(Log, self).save(*args, **kwargs)

                

    
        def __str__(self):
            return self.drone.nombre + str(self.timestep)
    
        def get_absolute_url(self):
            return reverse("_detail", kwargs={"pk": self.pk})

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Alquiler(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cliente} alquiló {self.drone} del {self.fecha_inicio} al {self.fecha_fin}"





class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.PositiveIntegerField()  # Duración estimada de la tarea en minutos
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class CoordenadaGPS(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"Latitud: {self.latitud}, Longitud: {self.longitud}"
    
class Monitoreo(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.FloatField(null=True)
    fotografia=models.ImageField(upload_to='images/foto',null=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Monitoreo de {self.tarea} con {self.drone}"

class Comentario(models.Model):
    monitoreo = models.ForeignKey(Monitoreo, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en {self.monitoreo}: {self.texto}"

