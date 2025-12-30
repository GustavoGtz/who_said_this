from typing import Protocol, Sequence, Tuple
from who.models import Message

"""
TODO: Completar esta implementación de clase.

ACLARACIÓN IMPORTANTE
El formato con el cual estoy trabajando estos módulos de Python sigue una metodología orientada
a PROTOCOLOS y MODELOS. Esta técnica se basa en dos conceptos: por una parte, los PROTOCOLOS son
formas de definir el COMPORTAMIENTO de los objetos en nuestro sistema; esto quiere decir que
podemos DECLARAR que esperamos que un objeto se comporte de una forma X al escribir la CABECERA
de sus métodos (describiendo así su comportamiento). Esto nos permite crear nuestro sistema
diciendo únicamente “tú dame un OBJETO que se COMPORTE de forma X y todo va a funcionar”; esto
nos permite crear un sistema más ESCALABLE y FÁCIL de CAMBIAR.

Por otro lado, los MODELOS son ENVOLTORIOS donde declaramos tipos de DATOS; estos serán utilizados
por los protocolos y por el sistema en general.

FIN DE LA ACLARACIÓN

Esta clase WhatsappMessagesManager sigue el protocolo MessagesManager. Para fines prácticos,
esta implementación debe cumplir con lo solicitado en las tres funciones principales. Todo lo demás,
como el constructor, variables de estado local o funciones auxiliares, queda libre a la propia
implementación (esta es la ventaja de trabajar con protocolos).

De manera general, esta clase será responsable de gestionar los mensajes que serán utilizados en la partida.
Si el ChatReader se encarga de leer y generar una lista de mensajes, MessagesManager se encarga de gestionarlos:
esto implica guardarlos en memoria, manipularlos, generar preguntas, etc.

Durante el tiempo de juego, esta clase será la encargada de generar la pool de mensajes para el
segundo filtro (si es que está activado) y también de generar las preguntas.

Los TODO exactos se encuentran abajo.

"""

class WhatsappMessagesManager:
    
    def __init__(self, messages: Sequence[Message], max_players : int):
        self.messages = messages
        self.max_players = max_players
        self.secs_per_round = 100 # default
        self.message_selection_method = "random" # default
            
    def get_max_players(self):
        return self.max_players

    def get_messages_number(self):
        return len(self.messages)
    
    def get_random(self, samples : int) -> Sequence[Message]:
        ...    

    def get_samples(self, sample_size: int, sample_count: int) -> Sequence[Sequence[Message]]:
        """
        Recibe dos parámetros: el número de muestras (sample_count)
        y el tamaño de cada una (sample_size).

        El procedimiento debe generar varias listas tomando mensajes directamente
        de la lista inicializada en el constructor y posteriormente formar las muestras.

        Es obligatorio ASEGURAR que cada mensaje aparezca UNA Y SOLO UNA VEZ en toda la secuencia
        de samples generados.

        Devuelve la lista de samples.
        """
        ...

    def generate_question(self) -> Tuple[Message, list[str]]:
        """
        Selecciona un mensaje aleatorio (o bajo el criterio elegido en esta implementación)
        desde la pool de mensajes almacenada como estado local.

        Luego genera una lista de opciones de respuesta, donde UNA es correcta
        y las demás son distractores.

        Antes de terminar, se debe eliminar el mensaje elegido de la pool interna
        para evitar que vuelva a aparecer.

        Devuelve una tupla con:
        - El mensaje pregunta
        - La lista de posibles respuestas
        """
        ...

    def set_messages(self, new_messages: Sequence[Message]) -> None:
        """
        Reemplaza el estado interno de los mensajes con la nueva lista proporcionada.
        """
        ...
