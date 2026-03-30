import requests
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint
from passerelle.utils.jsonresponse import APIError
from requests import RequestException


class LiegeCreances(BaseResource):
    """
    Connecteur App VDL Créances de Liège
    """

    url = models.URLField(
        max_length=255,
        blank=True,
        verbose_name="URL",
        help_text="URL de l'application VDL Créances",
    )
    api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Clé API",
    )
    api_description = (
        "Connecteur permettant d'intéragir avec l'application VDL Créances"
    )
    category = "Connecteurs iMio"

    class Meta:
        verbose_name = "Connecteur Liege Creances"

    @property
    def session(self):
        session = requests.Session()
        session.headers.update(
            {
                "X-Api-Key": self.api_key,
                "Accept": "application/json",
            }
        )
        return session

    @endpoint(
        methods=["get"],
        name="read-document",
        description="Récupérer les créances d'un redevable par numéro de document",
        long_description="Retourne la liste des créances pour un redevable et un numéro de document donnés",
        parameters={
            "user_id": {
                "description": "Identifiant du redevable",
                "example_value": "65112735187",
            },
            "numero_document": {
                "description": "Numéro de document",
                "example_value": "LR-99990001",
            },
            "requester_id": {
                "description": "Identifiant du demandeur",
                "example_value": "65112735187",
            },
        },
        perm="can_access",
        display_category="Document",
    )
    def read_document(self, request, user_id, numero_document, requester_id):
        url = f"{self.url}api/creances"  # Url et endpoint à contacter
        params = {
            "redevableId": user_id,
            "numeroDocument": numero_document,
            "requesterId": requester_id,
        }

        try:
            response = self.session.get(url, params=params)
        except RequestException as e:
            self.logger.warning(f"VDL Creances Connector Error: {e}")
            raise APIError(f"VDL Creances Connector Error: {e}")

        json_response = None
        try:
            json_response = response.json()
        except ValueError:
            self.logger.warning("VDL Creances Connector Error: bad JSON response")
            raise APIError("VDL Creances Connector Error: bad JSON response")

        try:
            response.raise_for_status()
        except RequestException as e:
            self.logger.warning(f"VDL Creances Connector Error: {e} {json_response}")
            raise APIError(f"VDL Creances Connector Error: {e} {json_response}")

        data = json_response.get("data")

        for index, creance in enumerate(data):
            id_list = f"{creance.get('vcs')}-{creance.get('invoice')}"
            text_list = f"{creance.get('libelle')} - {creance.get('dateEnvoi')} - {float(creance.get('montant', 0)):.2f}€"
            data[index]["id"] = id_list
            data[index]["text"] = text_list

        json_response["data"] = data
        return json_response
