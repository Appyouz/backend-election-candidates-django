from apps.core.models import Address
from apps.core.serializers import CreateAddressSerializer, UpdateAddressSerializer
from utils.core.general import update_model_instance


class AddressUtil:

    create_serializer = CreateAddressSerializer
    update_serializer = UpdateAddressSerializer

    @staticmethod
    def create_address(data, validate=True):
        if validate:
            serializer = AddressUtil.create_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

        address = Address(**data)
        address.save()

        return address

    @staticmethod
    def update_address(address, data, partial=False, validate=True):
        if validate:
            serializer = AddressUtil.update_serializer(
                instance=address, data=data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

        update_model_instance(address, **data)

        return address
