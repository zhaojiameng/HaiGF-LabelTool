
import collections
import damei as dm
# from hai_gui.hai import hai_client
logger = dm.get_logger('manager_dock')

class ManagerDock:  # 管理坞
    def __init__(self):
        self._hai = None
        # print('init ManagerDock')

    def set_manager_dock(self):
        self.manager_dock.setObjectName('manager_dock')
        self.manager_dock.setWidget(self.manager_list)
        self.manager_list.iconlist.itemDoubleClicked.connect(self.slot_ml_item_double_cliked)
        self.manager_list.itemCheckStateChanged.connect(self.slot_ml_item_check_state_changed)
        self.manager_list.iconlist.itemChanged.connect(self.slot_ml_item_check_state_changed)
    
    @property
    def ml(self):  # manage_list
        return self.manager_list  # 管理列表

    @property
    def hai(self):
        if self._hai is None:
            try:
                from hai_gui.hai import hai_client  # 适配无hai_client库
                self._hai = hai_client.HAIClient(self.hai_ip, self.hai_port)
                # print(self._haic.connect())
            except ImportError:
                logger.warning('hai_client not found')
                self._hai = None
        return self._hai

    def moduels_list2dict(self, moduels):
        moduels_dict = collections.OrderedDict()
        heads = moduels.pop(0)  # ['ID', 'TYPE', 'NAME', 'STATUS', 'TAG', 'INCLUDE', 'DESCRIPTION']
        for i, head in enumerate(heads):
            content = [f'{x[i]}' for x in moduels]
            moduels_dict[head] = content

        return moduels_dict

    def resource_manager(self):
        """
        资源管理，即算法、脚本等。
        逻辑：点击算法，如果已连接，刷新算法，未连接时，弹出连接服务端界面，连接。
        """
        logger.info('resource_manager clicked')

        if self.hai is None or not self.hai.connected:
            self.errorMessage(title='Connect Error', 
            message=f'Failed to connect to HAI server "{self.config["ip"]}:{self.config["port"]}", \
                    please check.')
            self.ml.clean()
            return 
        moduels = self.hai.hub.list(ret_fmt='json')
        print(moduels)
        moduels = self.moduels_list2dict(moduels)
        print(moduels)

        modals = moduels['NAME']
        modal_imgs = None

        self.ml.updateModals(mw=self, modals=modals, modal_imgs=modal_imgs)
        # self.ml.set_items(moduels)

    def search(self):
        logger.info('search clicked')

    def extension(self):
        logger.info('extension clicked')

    def slot_ml_item_double_cliked(self, item):
        """
        1 双击管理算法列表里的某个算法触发
        2 显示配置界面，或直接使用默认配置
        3 配置算法
        """
        logger.info(f'slot_ml_item_double_cliked {item} {type(item)}')
        alg_name = item.text()  # algorithm name
        self.hai.load_model(name=alg_name)
        model_icon = self.hai.model_icon()  # 模型图标
        model_config = self.hai.model_config()  # 键值对
        # print(model_config)
        
        
    def slot_ml_item_check_state_changed(self, item):
        logger.info(f'slot_ml_item_check_state_changed {item}')

    def slot_ml_item_changed(self, item):
        logger.info(f'slot_ml_item_changed {item}')

    def slot_magic_wand(self):
        logger.info('slot_magic')