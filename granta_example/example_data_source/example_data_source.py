import GRANTA_MIScriptingToolkit as gdl
import GdlUtils as gdlu

from force_bdss.api import BaseDataSource, DataValue, Slot


class ExampleDataSource(BaseDataSource):
    """Defines an example data source.
    This data source specifically performs a power operation
    on its input.
    """
    db_key = 'MI_FORCE'
    source_data_table_name = 'Source Data'
    test_results_table_name = 'Test Results'
    test_results_import_folder_name = 'Runs'

    #: This is where your computation happens.
    #: You receive the model, and a list of parameters
    #: that come from the MCO.
    #: Parameters are not plain numbers, but are instead instances
    #: of the DataValue class. This method must return a list
    #: of DataValue instances, whose number must match the number of
    #: output slots.
    def run(self, model, parameters):
        domain, username = model.domain_username.split("\\")
        session = gdl.GRANTA_MISession(
            model.url,
            username=username,
            domain=domain,
            password=model.password)

        search_result = gdlu.FindRecord(
            session,
            self.db_key,
            self.sourceDataTableName,
            "Row %s, Column %s" % (model.row, model.column))

        record_data = gdlu.GetRecordData(
            session,
            search_result.recordReference,
            attribNames=[model.attribute_name])

        values = gdlu.ReadValue(record_data.attributeValues[0])

        return [
            DataValue(
                type=model.cuba_type_out,
                value=values[0],
            )]

    #: If a data source is a function, the slots are the number of arguments
    #: it takes as input, and the number of entities it returns as output.
    #: This method must return a tuple of tuples. (input_tuple, output_tuple)
    #: Each tuple contains Slot instances. You can decide this information
    #: according to the model content, therefore if your data source returns
    #: different data depending on its settings, you can definitely handle
    #: this case.
    #: In this case, the data source is like a function
    #:
    #:                    a = pow(b)
    #:
    #: so it has one input slot and one output slot.
    #: a function like
    #:
    #:                a, b = func(m,n,o)
    #:
    #: has three input slots and two output slots.
    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
