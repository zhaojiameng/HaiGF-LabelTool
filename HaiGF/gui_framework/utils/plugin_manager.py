"""
插件管理器
"""
import os
import sys

class PluginManager(object):
    """
    插件管理器
    """
    def __init__(self):
        self._plugins = {}

    @property
    def plugins(self):
        return self._plugins

    @property
    def plugin_names(self):
        return list(self._plugins.keys())

    def register_plugin(self, plugin_name, plugin):
        """
        注册插件
        :param plugin_name: 插件名
        :param plugin: 插件对象
        """
        self._plugins[plugin_name] = plugin

    def get_plugin(self, plugin_name):
        """
        获取插件
        :param plugin_name: 插件名
        :return: 插件对象
        """
        return self._plugins.get(plugin_name)

    def get_all_plugins(self):
        """
        获取所有插件
        :return: 所有插件
        """
        return self._plugins

    def remove_plugin(self, plugin_name):
        """
        移除插件
        :param plugin_name: 插件名
        """
        self._plugins.pop(plugin_name)

    def clear(self):
        """
        清空插件
        """
        self._plugins.clear()