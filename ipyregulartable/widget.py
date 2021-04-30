# *****************************************************************************
#
# Copyright (c) 2020, the ipyregulartable authors.
#
# This file is part of the ipyregulartable library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import numpy as np
import pandas as pd
from ipywidgets import DOMWidget, CallbackDispatcher
from traitlets import (
    observe,
    validate,
    Bool,
    Dict,
    Instance,
    Integer,
    TraitError,
    Unicode,
)
from .datamodel import (
    DataModel,
    TwoBillionRows,
    NumpyDataModel,
    SeriesDataModel,
    DataFrameDataModel,
)
from ._version import __version__


_STYLER_KEYS = (
    "table",
    "thead",
    "tr",
    "th",
    "td",
    "theadtr",
    "theadth",
    "tbody",
    "tbodytr",
    "tbodyth",
)


class RegularTableWidget(DOMWidget):
    _model_name = Unicode("RegularTableModel").tag(sync=True)
    _model_module = Unicode("ipyregulartable").tag(sync=True)
    _model_module_version = Unicode("^" + __version__).tag(sync=True)
    _view_name = Unicode("RegularTableView").tag(sync=True)
    _view_module = Unicode("ipyregulartable").tag(sync=True)
    _view_module_version = Unicode("^" + __version__).tag(sync=True)

    datamodel = Instance(DataModel)

    height = Integer(default_value=250).tag(sync=True)

    sort = Dict(default_value={}).tag(sync=True)
    filter = Dict(default_value={}).tag(sync=True)

    css = Dict(default_value={}).tag(sync=True)
    styler = Dict(default_value={}).tag(sync=True)

    _data = Dict(default_value={}).tag(sync=True)
    _editable = Bool(default_value=False).tag(sync=True)

    def __init__(self, datamodel=None, log_js_errors=True):
        # super
        super(RegularTableWidget, self).__init__()

        # install data model
        if datamodel is None:
            # Demo
            self.datamodel = TwoBillionRows()
        elif isinstance(datamodel, (DataModel,)):
            self.datamodel = datamodel
        elif isinstance(datamodel, np.ndarray):
            self.datamodel = NumpyDataModel(datamodel)
        elif isinstance(datamodel, pd.Series):
            self.datamodel = SeriesDataModel(datamodel)
        elif isinstance(datamodel, pd.DataFrame):
            self.datamodel = DataFrameDataModel(datamodel)
        else:
            raise Exception("Unsupported data model: {}".format(datamodel))

        # set self for draw callbacks
        self.datamodel._setWidget(self)

        # for click events
        self._click_handlers = CallbackDispatcher()

        # for edit events
        self._edit_handlers = CallbackDispatcher()

        # hook in custom messages
        self.on_msg(self._handle_custom_msg)

        # log js errors?
        self._log_js_errors = log_js_errors

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def on_edit(self, callback, remove=False):
        self._edit_handlers.register_callback(callback, remove=remove)

    def click(self, value):
        self._click_handlers(self, value)

    def edit(self, value):
        self._edit_handlers(self, value)

    @observe("datamodel")
    def _datamodel_changed(self, change):
        self.draw()

    def _jserrors(self, error):
        if error and self._log_js_errors:
            raise Exception(error)

    def _handle_custom_msg(self, content, buffers=None):
        if content.get("event", "") == "click":
            self.click(content.get("value", ""))

        elif content.get("event", "") == "dataslice":
            self.dataslice(*content.get("value", []))

        elif content.get("event", "") == "editable":
            self.editable(*content.get("value", []))

        elif content.get("event", "") == "write":
            self.datamodel.write(*content.get("value", []))
            self.edit(content.get("value", ""))

        elif content.get("event", "") == "sort":
            self.datamodel.sort(*content.get("value", []))

        elif content.get("event", "") == "filter":
            self.datamodel.filter(*content.get("value", []))

        elif content.get("event", "") == "errors":
            self._jserrors(content.get("value", ""))

    def dataslice(self, x0, y0, x1, y1):
        self._data = {
            "num_rows": self.datamodel.rows(),
            "num_columns": self.datamodel.columns(),
            "column_headers": self.datamodel.columnheaders(x0, y0, x1, y1),
            "row_headers": self.datamodel.rowheaders(x0, y0, x1, y1),
            "data": self.datamodel.dataslice(x0, y0, x1, y1),
        }
        self.post({"type": "data"})
        return self._data

    def editable(self, x, y):
        self._editable = self.datamodel.editable(x, y)
        self.post({"type": "editable"})
        return self._editable

    def post(self, msg):
        self.send(msg)

    def draw(self):
        self.send({"type": "draw"})

    def setData(self, data):
        self.datamodel.setData(data)
        self.draw()

    @validate("css")
    def _validate_css(self, proposal):
        proposal = proposal["value"]

        if not isinstance(proposal, dict):
            raise TraitError("css needs to be dict")

        for key in proposal.keys():
            if key not in _STYLER_KEYS:
                raise TraitError("Unrecognized key: {}".format(key))

        return proposal

    @validate("styler")
    def _validate_styler(self, proposal):
        proposal = proposal["value"]

        if not isinstance(proposal, dict):
            raise TraitError("styler needs to be dict")

        for key in proposal.keys():
            if key not in _STYLER_KEYS:
                raise TraitError("Unrecognized key: {}".format(key))
            if not isinstance(proposal[key], dict):
                raise TraitError("styler values need to be dict")
            if not list(proposal[key].keys()) == ["expression", "style"]:
                raise TraitError("Invalid trait: {}".format(proposal[key]))

        return proposal
