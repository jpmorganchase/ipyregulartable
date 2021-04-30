/******************************************************************************
 *
 * Copyright (c) 2020, the ipyregulartable authors.
 *
 * This file is part of the ipyregulartable library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
/* eslint-disable @typescript-eslint/explicit-member-accessibility */
/* eslint-disable @typescript-eslint/tslint/config */
/* eslint-disable @typescript-eslint/explicit-function-return-type */
import {DOMWidgetModel, ISerializers} from "@jupyter-widgets/base";
import {MODULE_VERSION} from "./version";


export
class RegularTableModel extends DOMWidgetModel {
  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static modelName = "RegularTableModel";
  static modelModule = "ipyregulartable";
  static modelModuleVersion = MODULE_VERSION;
  static viewName = "RegularTableView";   // Set to null if no view
  static viewModule = "ipyregulartable";   // Set to null if no view
  static viewModuleVersion = MODULE_VERSION;

  public defaults() {
    return {...super.defaults(),
      _model_name: RegularTableModel.modelName,
      _model_module: RegularTableModel.modelModule,
      _model_module_version: RegularTableModel.modelModuleVersion,
      _view_name: RegularTableModel.viewName,
      _view_module: RegularTableModel.viewModule,
      _view_module_version: RegularTableModel.viewModuleVersion,

      height: 200,
      css: {
        table: "", // overall table styles
        thead: "", // header
        theadtr: "", // header row
        theadth: "", // entries in header row (column headers)
        tbody: "", // body
        tbodytr: "", // rows in body
        tbodyth: "", // headers in body (row headers)
        tbodytd: "", // entries
      },
      styler: {
        table: {
          expression: [],
          style: [],
        },
        thead: {
          expression: [],
          style: [],
        },
        tr: {
          expression: [],
          style: [],
        },
        th: {
          expression: [],
          style: [],
        },
        td: {
          expression: [],
          style: [],
        },
        theadtr: {
          expression: [],
          style: [],
        },
        theadth: {
          expression: [],
          style: [],
        },
        tbody: {
          expression: [],
          style: [],
        },
        tbodytr: {
          expression: [],
          style: [],
        },
        tbodyth: {
          expression: [],
          style: [],
        },
      },
      sort: {},
      filter: {},
      _data: {},
      _editable: false,
    };
  }
}

