# class ProductSearchView(SearchAPIView):
#     serializer_class = ProductSerializer
#     document_class   = mprod_exp180Document

#     def generate_q_expression(self, query):
#         return Q(
#                 'multi_match', query=query,
#                 fields=[
#                     'title',
#                     'description'
#                 ], fuzziness='auto')