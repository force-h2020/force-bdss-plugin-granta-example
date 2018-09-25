from force_bdss.api import BaseDataSourceFactory

from .example_data_source_model import ExampleDataSourceModel
from .example_data_source import ExampleDataSource


class ExampleDataSourceFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "data_retriever"

    def get_name(self):
        return "GRANTA Data Retriever (Test)"

    def get_model_class(self):
        return ExampleDataSourceModel

    def get_data_source_class(self):
        return ExampleDataSource
