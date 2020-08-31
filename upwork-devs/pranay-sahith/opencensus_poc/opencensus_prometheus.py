import random
import time
from pprint import pprint
import logging

from opencensus.ext.prometheus import stats_exporter as prometheus
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_key as tag_key_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.tags import tag_value as tag_value_module
from opencensus.stats import aggregation_data

class OpenCensusPrometheus:

    def __init__(self, test_id):
        logging.info(f"setting up prometheus for test id: {test_id}")
        self.test_id = test_id
        # create tags
        self.tag_map = tag_map_module.TagMap()
        self.create_tags("TEST_ID", test_id)
        stats = stats_module.stats
        self.view_manager = stats.view_manager
        self.stats_recorder = stats.stats_recorder
        exporter = prometheus.new_stats_exporter(
            prometheus.Options(namespace="glasswall"))
        self.view_manager.register_exporter(exporter)
        # create measurements and views
        home_page_measurement = self.create_measurement_view("home_page")
        download_brochure_measurement = self.create_measurement_view("download_brochure")
        self.measurements = {"home_page": home_page_measurement,
                             "download_brochure": download_brochure_measurement}
        aggregation_data.SumAggregationDataFloat = aggregation_data.SumAggregationData
        

    def create_measurement_view(self, measurement_name):
        "creates a measurement and a view"
        tg_key = tag_key_module.TagKey("TEST_ID")
        measurement = measure_module.MeasureInt(
            f"gw_m_{measurement_name}_response", "response time of the home page", "s")
        view_name = f"views_{measurement_name}_response"
        aggregation = aggregation_module.LastValueAggregation()
        view = view_module.View(
            view_name, f"glasswall {measurement_name} response time", [tg_key],
            measurement, aggregation)
        # Register view.
        self.view_manager.register_view(view)
        return measurement


    def get_stats_recorder(self):
        "returns a stats recorder"
        return self.stats_recorder

    def create_tags(self, tag_name, tag_value):
        "create tags to group and filter metrics of a particular run"
        tg_key = tag_key_module.TagKey(tag_name)
        tag_value = tag_value_module.TagValue(tag_value)
        self.tag_map.insert(tg_key, tag_value)

    def get_tag_map(self):
        return self.tag_map

    def set_measurement(self, measurement_name, measurement):
        "record measurements and send to prometheus"
        measure_map = self.get_stats_recorder().new_measurement_map()
        measure_map.measure_int_put(self.measurements[measurement_name], measurement)
        measure_map.record(self.get_tag_map())


if __name__ == '__main__':
    ocp = OpenCensusPrometheus()
    
