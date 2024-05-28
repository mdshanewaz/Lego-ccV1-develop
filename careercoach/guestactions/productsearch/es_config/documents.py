# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
# from django_elasticsearch_dsl import (
#     fields,
#     Index,
# )

# from resumeweb.models import mprod_exp180


# @registry.register_document
# class mprod_exp180Document(Document):
#     class Index:
#         name = 'mango'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }

#     class Django:
#         model = mprod_exp180
#         fields = [
#          'title',
#          'description',
#         ]
