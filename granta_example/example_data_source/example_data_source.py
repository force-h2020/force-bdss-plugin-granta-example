import logging
import requests
import granta_example.mipy as mi

from force_bdss.api import BaseDataSource, DataValue, Slot

logger = logging.getLogger(__name__)


class ExampleDataSource(BaseDataSource):
    def run(self, model, parameters):
        logger.info("Executing ExampleDataSource")
        session = requests.Session()
        session.auth = (model.login, model.password)
        session.headers.update({
            'content-type': 'text/xml;charset=UTF-8'
        })
        name = "Row %s, Column %s" % (model.row, model.column)
        record = mi.recordNameSearch(
            session, model.url, model.db_key,
            model.source_data_table_name, name)
        data = mi.exportRecordData(
            session, model.url, model.db_key,
            model.source_data_table_name, record, [model.attribute_name])

        value = float(data[model.attribute_name].xpath(
            "descendant::gbt:PointDataValue/gbt:Point/gbt:Value",
            namespaces=mi.ns
        )[0].text)
        logger.info("Obtained data value: {}".format(value))

        return [
            DataValue(
                type=model.cuba_type_out,
                value=value,
            )]

    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
