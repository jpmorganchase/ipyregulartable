# *****************************************************************************
#
# Copyright (c) 2020, the ipyregulartable authors.
#
# This file is part of the ipyregulartable library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
from abc import ABCMeta, abstractmethod
from six import with_metaclass


class DataModel(with_metaclass(ABCMeta)):
    _widget = None

    def _setWidget(self, widget):
        self._widget = widget

    def draw(self):
        """Call back to parent widget's `draw` method to
        rerender the table"""
        if self._widget is not None:
            self._widget.draw()

    def setData(self, data):
        """optional setData method"""

    @abstractmethod
    def editable(self, x, y):
        """Given an (x,y) coordinate, return if its editable or not"""

    @abstractmethod
    def rows(self):
        """return total number of rows"""

    @abstractmethod
    def columns(self):
        """return total number of columns"""

    @abstractmethod
    def dataslice(self, x0, y0, x1, y1):
        """get slice of data from (x0, y0) to (x1, y1) inclusive"""

    def rowheaders(self, x0, y0, x1, y1):
        """return column headers for data"""
        return [[str(_)] for _ in range(y0, y1)]

    def columnheaders(self, x0, y0, x1, y1):
        """return column headers for data"""
        return [[str(_)] for _ in range(x0, x1)]

    def sort(self, column, how):
        """sort data by value.

        Args:
            column (int): column to sort
            how (str): "asc", "desc", or ""
        """
    
    def filter(self, column, how):
        """filter data by value.

        Args:
            column (int): column to sort
                how (str): fragment
        """

    def write(self, x, y, value):
        """write event"""
