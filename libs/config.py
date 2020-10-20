# -*- coding: utf-8 -*-
"""
Yuuki_Libs
(c) 2020 Star Inc.
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import os

import yaml


class Yuuki_Config:
    """

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !! DO NOT TOUCH DEFAULT SETTINGS !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    Please config the value you want to set though `config.yaml`.
    It will overwrite these settings.

    """

    connectInfo = {
        "Host": "",
        "Command_Path": "",
        "LongPoll_path": "",
    }

    connectHeader = {
        "X-Line-Application": "",
        "X-Line-Access": "",
        "User-Agent": ""
    }

    systemConfig = {
        "name": "Yuuki",
        "version": "v6.5.3-beta_RC0",
        "version_check": True,
        "project_url": "https://tinyurl.com/syb-yuuki",
        "man_page": "https://tinyurl.com/yuuki-manual",
        "privacy_page": "OpenSource - Licensed under MPL 2.0",
        "copyright": "(c)2020 Star Inc.",

        "Seq": 0,
        "Admin": [],
        "Advanced": False,
        "WebAdmin": False,  # Advanced Mode Required
        "MDS_Port": 2019,
        "WebAdmin_Port": 2020,
        "SecurityService": False,
        "Hour_KickLimit": 10,
        "Hour_CancelLimit": 10,
        "Default_Language": "en",
        "GroupMebers_Demand": 100,
        "helper_LINE_ACCESS_KEYs": [],
    }

    def __init__(self, config_path="config.yaml"):
        assert os.path.isfile(config_path), "The config file, `config.yaml` was not found."
        with open(config_path, "r") as configfile:
            self.config = yaml.load(configfile, Loader=yaml.FullLoader)
        self._yuuki_config()

    def _yuuki_config(self):
        assert self.config is not None, "Invalid config file"
        if "Yuuki" in self.config:
            for key in self.config["Yuuki"]:
                if key in self.systemConfig:
                    self.systemConfig[key] = self.config["Yuuki"][key]
        return self._server_config()

    def _server_config(self):
        if "Server" in self.config.get("LINE"):
            for key in self.config["LINE"]["Server"]:
                if key in self.connectInfo:
                    self.connectInfo[key] = self.config["LINE"]["Server"][key]
        return self._account_config()

    def _account_config(self):
        if "Account" in self.config.get("LINE"):
            for key in self.config["LINE"]["Account"]:
                if key in ["X-Line-Application", "User-Agent"]:
                    self.config["LINE"]["Account"][key] = self.config["LINE"]["Account"][key].replace("\\t", "\t")
                if key in self.connectHeader:
                    self.connectHeader[key] = self.config["LINE"]["Account"][key]

        if "helper_LINE_ACCESS_KEYs" in self.config.get("LINE"):
            self.systemConfig["helper_LINE_ACCESS_KEYs"] = self.config["LINE"]["helper_LINE_ACCESS_KEYs"]
