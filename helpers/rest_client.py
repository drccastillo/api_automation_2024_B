import json
import logging

import requests

from config.config import headers_booker
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:

    def __init__(self, headers=headers_booker):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def request(self, method_name, url, body=None):
        """
        Realiza una solicitud HTTP y maneja la respuesta.
        :param method_name: El nombre del método HTTP (GET, POST, etc.).
        :param url: La URL a la que se hará la solicitud.
        :param body: El cuerpo de la solicitud (opcional).
        :return: Un diccionario con la información de la respuesta.
        """
        response_dict = {}
        response = None  # Inicializar la variable de respuesta

        try:
            response = self.select_method(method_name, self.session)(url=url, json=body)
            LOGGER.debug("Response to request: %s", response.text)
            LOGGER.debug("Status Code: %s", response.status_code)
            response.raise_for_status()
            response_dict["status_code"] = response.status_code

            if hasattr(response, "headers"):
                LOGGER.debug("Response Headers: %s", response.headers)
                response_dict["headers"] = response.headers

            # Si la respuesta contiene datos, procesarla
            if response.text:
                if response.ok:
                    try:
                        response_dict["body"] = json.loads(response.text)
                    except json.JSONDecodeError:
                        # Si la respuesta no es un JSON válido, asignarla como texto sin procesar
                        response_dict["body"] = response.text
                else:
                    response_dict["body"] = {"msg": f"{response.text}"}
            else:
                response_dict["body"] = {
                    "msg": "No hay contenido en el cuerpo de la respuesta"
                }

        except requests.exceptions.HTTPError as http_error:
            LOGGER.error("HTTP Error: %s", http_error)
            response_dict["status_code"] = response.status_code if response else None
        except requests.exceptions.RequestException as request_error:
            LOGGER.error("Request Error: %s", request_error)
            response_dict["status_code"] = response.status_code if response else None
        finally:
            if response:
                response.close()

        return response_dict

    @staticmethod
    def select_method(method_name, session):
        """
        Selecciona el método REST con el objeto de sesión.
        :param method_name: El nombre del método HTTP (GET, POST, etc.).
        :param session: La sesión de la solicitud.
        :return: La función correspondiente al método HTTP.
        """
        methods = {
            "get": session.get,
            "post": session.post,
            "delete": session.delete,
            "put": session.put,
        }
        return methods.get(method_name)
