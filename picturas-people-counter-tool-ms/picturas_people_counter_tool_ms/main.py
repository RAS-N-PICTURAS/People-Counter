import logging

from .config import PICTURAS_LOG_LEVEL
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .people_counter_request_message import PeopleCounterRequestMessage
from .people_counter_result_message import PeopleCounterResultMessage
from .people_counter_tool import PeopleCounterTool

# Configuração de logs
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    # Conectar ao RabbitMQ
    connection, channel = message_queue_connect()

    # Inicializar a ferramenta
    tool = PeopleCounterTool()

    # Definir as classes de mensagens de solicitação e resultado
    request_msg_class = PeopleCounterRequestMessage
    result_msg_class = PeopleCounterResultMessage

    # Inicializar o processador de mensagens
    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        # Iniciar o processamento de mensagens
        message_processor.start()
    except KeyboardInterrupt:
        # Parar o processamento em caso de interrupção manual
        message_processor.stop()

    # Fechar a conexão com o RabbitMQ
    connection.close()
