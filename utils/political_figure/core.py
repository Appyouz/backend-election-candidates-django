from apps.political_figure.models import PoliticalFigure
from apps.political_figure.serializers import (
    CreatePoliticalFigureSerializer,
    UpdatePoliticalFigureSerializer,
)
from django.db import transaction

from utils.core.address_util import AddressUtil
from utils.core.general import update_model_instance


class PoliticalFigureUtil:
    """
    Single Source of truth for data mutation and some fetch operation for political figure
    """

    create_serializer = CreatePoliticalFigureSerializer
    update_serializer = UpdatePoliticalFigureSerializer

    @staticmethod
    def create_political_figure(data):
        """
        Creates and returns political figure.
        """
        print(data)
        serializer = PoliticalFigureUtil.create_serializer(data=data)

        # serializer's ValidationError is automatically handled in exception handler
        serializer.is_valid(raise_exception=True)

        political_figure_data = serializer.validated_data

        # pop address data
        home_address_data = political_figure_data.pop("home_address")
        current_address_data = political_figure_data.pop("current_address")

        with transaction.atomic():
            # create addresses first
            # validate False cause we've already validated address data
            home_address = AddressUtil.create_address(home_address_data, validate=False)
            current_address = AddressUtil.create_address(
                current_address_data, validate=False
            )

            # prepare data for political figure
            political_figure_data["home_address"] = home_address
            political_figure_data["current_address"] = current_address

            political_figure = PoliticalFigure(**political_figure_data)
            political_figure.save()

        return political_figure

    @staticmethod
    def update_political_figure(political_figure: PoliticalFigure, data):
        """
        Updates and returns political figure.
        """

        home_address = political_figure.home_address
        current_address = political_figure.current_address
        # Store original photo for potential deletion
        old_photo = political_figure.photo

        serializer = PoliticalFigureUtil.update_serializer(
            instance=political_figure, data=data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        political_figure_data = serializer.validated_data

        # print(political_figure_data, "political figure data")

        home_address_data = political_figure_data.pop("home_address", None)
        current_address_data = political_figure_data.pop("current_address", None)

        # new_photo None means key was passed, but value was None. So, delete old photo and set photo to None
        # new_photo == "__photo_key_was_not_provided__" means key was not passed. So, keep old photo and do nothing
        # new_photo == anything else means key was passed and value was not None. So, delete old photo and set new photo
        new_photo = political_figure_data.get("photo", "__photo_key_was_not_provided__")

        with transaction.atomic():
            if home_address_data:
                home_address = AddressUtil.update_address(
                    home_address, home_address_data, partial=True, validate=False
                )

            if current_address_data:
                current_address = AddressUtil.update_address(
                    current_address, current_address_data, partial=True, validate=False
                )

            update_model_instance(political_figure, **political_figure_data)

            # handle image deletion
            # Handle photo logic before updating the model
            # handle image deletion / replacement
            if new_photo is None:
                print("new photo is None (no photo ), deleting old photo")
                # case: explicitly set to null -> delete old photo
                transaction.on_commit(lambda photo=old_photo: photo.delete(save=False))

            elif new_photo == "__photo_key_was_not_provided__":
                print("new photo is __photo_key_was_not_provided__, doing nothing...")
                # do nothing
                pass
            else:
                print(
                    "new photo is not None or __photo_key_was_not_provided__, deleting old photo...; new photo has already been set"
                )
                # this means new_photo was neither None nor "__photo_key_was_not_provided__", so delete old photo and set new photo (set new photo is already done in update_model_instance)
                # new_photo was provided, so delete old photo
                # case: new image uploaded -> delete old one
                if old_photo:
                    transaction.on_commit(
                        lambda photo=old_photo: photo.delete(save=False)
                    )

        # raise Exception("temporary exception")
        return political_figure

    @staticmethod
    def delete_political_figure(political_figure: PoliticalFigure):
        with transaction.atomic():
            home_address = political_figure.home_address
            current_address = political_figure.current_address

            home_address.delete()
            current_address.delete()
            political_figure.delete()
