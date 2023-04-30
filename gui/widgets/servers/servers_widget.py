from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QComboBox,
    QPushButton,
    QFormLayout,
    QSpinBox,
    QCheckBox,
    QLineEdit,
    QGroupBox,
    QScrollArea
)
from PyQt5.QtCore import Qt, QEventLoop

from gui import threads
from minecraft_server import version, server_properties, exceptions
from gui.widgets.servers.servers_selection import ServerSelection
from gui.widgets.servers.server_settings_widget import ServerSettingsWidget
from gui.widgets.servers.server_properties_widget import ServerPropertiesWidget
from gui.widgets.combo_box import ComboBox
from minecraft_server.server import (
    Server,
    ServerSettings,
    start_server,
    get_servers,
    get_default_settings
)
import os
import glob


class ServersWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.thread_handler = parent.thread_handler
        self.settings = parent.settings
        self.progress_bar = parent.progress_bar
        self.console_widget = parent.running_servers_widget.console_widget
        self.toolbar_widget = parent.toolbar_widget3

        self.tabs = QTabWidget()
        self.tabs.addTab(self.start_servers_tab(), "Servers")
        self.tabs.addTab(self.create_new_server_tab(), "New server")

        self.servers_label = QLabel("Servers")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.servers_label)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)


    def start_servers_tab(self):
        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab_layout.setAlignment(Qt.AlignTop)
        servers_tab.setLayout(servers_tab_layout)

        self.servers = get_servers(self.settings.data_location)
        self.servers_selection = ServerSelection(
            self.servers, self.thread_handler, start_server, self.console_widget, self.toolbar_widget)
        servers_tab_layout.addWidget(self.servers_selection)
        return servers_tab


    def create_new_server_tab(self):
        server_creation = QWidget()
        server_creation_layout = QVBoxLayout()
        server_creation.setLayout(server_creation_layout)

        versions = version.get_minecraft_versions()

        self.header_layout = QHBoxLayout()

        self.version_select = ComboBox()
        self.version_select.addItems(versions)

        self.create_button = QPushButton("Create server")
        self.create_button.clicked.connect(self.create_server)

        self.settings_group = ServerSettingsWidget()

        self.config_group = ServerPropertiesWidget()

        self.name_lineedit = QLineEdit()
        self.name_lineedit.setText(f"Minecraft server")

        self.header_layout.addWidget(self.name_lineedit)
        self.header_layout.addWidget(self.version_select)

        server_creation_layout.addLayout(self.header_layout)
        server_creation_layout.addWidget(self.create_button)
        server_creation_layout.addWidget(self.settings_group)
        server_creation_layout.addWidget(self.config_group)

        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab_layout.setAlignment(Qt.AlignTop)
        servers_tab.setLayout(servers_tab_layout)
        servers_tab_layout.addWidget(server_creation)
        return servers_tab


    def refresh(self):
        self.servers = get_servers(self.settings.data_location)
        self.servers_selection.refresh(self.servers)
        print('refresh servers')


    def create_server(self):
        settings, properties = self.get_server_values()
        version = settings['version']

        server_data_path = os.path.join(
            self.settings.data_location, settings['name'])

        if os.path.exists(server_data_path):
            raise Exception("Server data path already exists")  # TODO

        os.makedirs(server_data_path)

        download_thread = threads.DownloadThread(version, server_data_path)
        download_thread.increment_progress_bar_value.connect(self.progress_bar.increment_value)
        download_thread.set_maximum_progress_bar_value.connect(self.progress_bar.set_maximum)
        download_thread.set_progress_bar_description.connect(self.progress_bar.set_description)
        download_thread.reset_progress_bar.connect(self.progress_bar.reset)
        download_thread.show_progress_bar.connect(self.progress_bar.show)

        loop = QEventLoop()
        download_thread.download_finished.connect(loop.quit)
        self.thread_handler.start_thread(download_thread)
        loop.exec_()

        self.progress_bar.start_loading()

        jar_pattern = '*.jar'
        jar_files = []
        jar_files = glob.glob(os.path.join(server_data_path, jar_pattern))

        # find jar file in server data path
        try:
            jar_path = jar_files[0]

            server_settings = ServerSettings()
            self.set_server_settings(server_settings, settings)
            server = Server(server_data_path, server_settings, jar_path)

            server_properties.create(server_data_path, properties)
            server.agree_to_eula()
        except IndexError:
            raise exceptions.JarNotFound("No jar file found in server data path")

        self.progress_bar.stop_loading()
        self.progress_bar.hide()

        self.refresh()


    def set_server_settings(self, server_settings: ServerSettings, settings: dict):
        server_settings.Xmx = settings.get('xmx')
        server_settings.Xms = settings.get('xms')
        server_settings.bonusChest = settings.get('bonus-chest')
        server_settings.eraseCache = settings.get('erase-cache')
        server_settings.forceUpgrade = settings.get('force-upgrade')
        server_settings.safeMode = settings.get('safe-mode')
        server_settings.universe = settings.get('universe')


    def get_server_values(self):
        settings = {}
        settings['name'] = self.name_lineedit.text()
        settings['version'] = self.version_select.currentText()
        settings['xmx'] = self.Xmx_spinbox.value()
        settings['xms'] = self.Xms_spinbox.value()
        settings['bonus-chest'] = self.bonus_chest_checkbox.isChecked()
        settings['erase-cache'] = self.erase_cache_checkbox.isChecked()
        settings['force-upgrade'] = self.force_upgrade_checkbox.isChecked()
        settings['safe-mode'] = self.safe_mode_checkbox.isChecked()
        settings['universe'] = self.universe_lineedit.text()

        properties = {}
        properties['allow-flight'] = self.allow_flight_checkbox.isChecked()
        properties['allow-nether'] = self.allow_nether_checkbox.isChecked()
        properties['broadcast-console-to-ops'] = self.broadcast_console_to_ops_checkbox.isChecked()
        properties['broadcast-rcon-to-ops'] = self.broadcast_rcon_to_ops_checkbox.isChecked()
        properties['difficulty'] = self.difficulity_combobox.currentText()
        properties['enable-command-block'] = self.enable_command_block_checkbox.isChecked()
        properties['enable-jmx-monitoring'] = self.enable_jmx_monitoring_checkbox.isChecked()
        properties['enable-query'] = self.enable_query_checkbox.isChecked()
        properties['enable-rcon'] = self.enable_rcon_checkbox.isChecked()
        properties['enable-status'] = self.enable_status_checkbox.isChecked()
        properties['enforce-secure-profile'] = self.enforce_secure_profile_checkbox.isChecked()
        properties['enforce-whitelist'] = self.enforce_whitelist_checkbox.isChecked()
        properties['entity-broadcast-range-percentage'] = self.entity_broadcast_range_percentage_spinbox.value()
        properties['force-gamemode'] = self.force_gamemode_checkbox.isChecked()
        properties['function-permission-level'] = self.function_permission_level_spinbox.value()
        properties['gamemode'] = self.gamemode_combobox.currentText()
        properties['generate-structures'] = self.generate_structures_checkbox.isChecked()
        properties['generator-settings'] = self.generator_settings_lineedit.text()
        properties['hardcore'] = self.hardcore_checkbox.isChecked()
        properties['hide-online-players'] = self.hide_online_players_checkbox.isChecked()
        properties['initial-disabled-packs'] = self.initial_disabled_packs_lineedit.text()
        properties['initial-enabled-packs'] = self.initial_enabled_packs_lineedit.text()
        properties['level-name'] = self.level_name_lineedit.text()
        properties['level-seed'] = self.level_seed_lineedit.text()
        properties['level-type'] = self.level_type_lineedit.text()
        properties['max-chained-neighbor-updates'] = self.max_chained_neighbor_updates_spinbox.value()
        properties['max-players'] = self.max_players_spinbox.value()
        properties['max-tick-time'] = self.max_tick_time_spinbox.value()
        properties['max-world-size'] = self.max_world_size_spinbox.value()
        properties['motd'] = self.motd_lineedit.text()
        properties['network-compression-threshold'] = self.network_compression_threshold_spinbox.value()
        properties['online-mode'] = self.online_mode_checkbox.isChecked()
        properties['op-permission-level'] = self.op_permission_level_spinbox.value()
        properties['player-idle-timeout'] = self.player_idle_timeout_spinbox.value()
        properties['prevent-proxy-connections'] = self.prevent_proxy_connections_checkbox.isChecked()
        properties['pvp'] = self.pvp_checkbox.isChecked()
        properties['query.port'] = self.query_port_spinbox.value()
        properties['rate-limit'] = self.rate_limit_spinbox.value()
        properties['rcon.password'] = self.rcon_password_lineedit.text()
        properties['rcon.port'] = self.rcon_port_spinbox.value()
        properties['require-resource-pack'] = self.require_resource_pack_checkbox.isChecked()
        properties['resource-pack'] = self.resource_pack_prompt_lineedit.text()
        properties['resource-pack-prompt'] = self.resource_pack_sha1_lineedit.text()
        properties['resource-pack-sha1'] = self.resource_pack_sha1_lineedit.text()
        properties['server-ip'] = self.server_ip_lineedit.text()
        properties['server-port'] = self.server_port_spinbox.value()
        properties['simulation-distance'] = self.simulation_distance_spinbox.value()
        properties['spawn-animals'] = self.spawn_animals_checkbox.isChecked()
        properties['spawn-monsters'] = self.spawn_monsters_checkbox.isChecked()
        properties['spawn-npcs'] = self.spawn_npcs_checkbox.isChecked()
        properties['spawn-protection'] = self.spawn_protection_spinbox.value()
        properties['sync-chunk-writes'] = self.sync_chunk_writes_checkbox.isChecked()
        properties['text-filtering-config'] = self.text_filtering_config_lineedit.text()
        properties['use-native-transport'] = self.use_native_transport_checkbox.isChecked()
        properties['view-distance'] = self.view_distance_spinbox.value()
        properties['white-list'] = self.white_list_checkbox.isChecked()

        properties = server_properties.stringify(properties)

        return settings, properties
