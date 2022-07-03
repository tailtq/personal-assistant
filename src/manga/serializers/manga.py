from rest_framework import serializers

from manga.services import MangaService


class MangaSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField()
    thumbnail_url = serializers.CharField()
    other_names = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._service = MangaService()

    def create(self, validated_data):
        return self._service.create({
            "name": validated_data["name"],
            "thumbnail_url": validated_data["thumbnail_url"],
            "other_names": validated_data.get("other_names", [])
        })

    def update(self, instance, validated_data):
        return self._service.save(instance, validated_data)

    def validate(self, attrs):
        # validate resource exists
        if "_id" in self.context:
            self.instance = self._service.get_by_id(self.context["_id"])
            if not self.instance:
                raise serializers.ValidationError({"instance": ["Resource not found"]})
        # validate duplicate name
        if self._service.check_manga_exist(attrs["name"], self.context.get("_id")):
            raise serializers.ValidationError({"name": ["Manga exists"]})
        return attrs
