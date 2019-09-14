from ambrogio_mock import AmbrogioMock
from plugins.treasurer import Treasurer


class TestTresurer(object):
    plugin = None
    ambrogio = None

    def setup_method(self, f):
        self.ambrogio = AmbrogioMock()
        self.plugin = Treasurer()
        self.plugin.init_plugin(self.ambrogio)
