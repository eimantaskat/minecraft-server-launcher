from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QTabWidget, QComboBox, QPushButton, QFormLayout, QSpinBox, QCheckBox, QLineEdit, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from ... import threads
from minecraft_server import Settings, version, server_properties, downloader
from .servers_selection import ServerSelection
from minecraft_server.server import Server, ServerSettings, start_server, get_servers, get_default_settings
import os

class ServersWidget(QWidget):
    def __init__(self, settings: Settings, thread_handler: threads.ThreadHandler):
        super().__init__()
        self.thread_handler = thread_handler
        self.settings = settings

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_servers_tab(), "Servers")
        self.tabs.addTab(self.create_new_server_tab(), "New server")

        self.servers_label = QLabel("Servers")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.servers_label)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    def create_servers_tab(self):
        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab_layout.setAlignment(Qt.AlignTop)
        servers_tab.setLayout(servers_tab_layout)

        self.servers = get_servers(self.settings.data_location)
        self.servers_selection = ServerSelection(self.servers, self.thread_handler, start_server)
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

        self.settings_group = QGroupBox("Server Settings")
        self.settings_layout = self.create_settings_layout()
        self.settings_group.setLayout(self.settings_layout)

        self.config_group = QGroupBox("Server configuration")
        self.config_scroll_ared = QScrollArea
        self.config_layout = self.create_config_layout()
        self.config_group.setLayout(QVBoxLayout())
        self.config_group.layout().addWidget(self.config_layout)

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

    def create_config_layout(self):
        form_layout = QFormLayout()

        self.allow_flight_checkbox = QCheckBox()
        self.allow_flight_checkbox.setChecked(False)

        self.allow_nether_checkbox = QCheckBox()
        self.allow_nether_checkbox.setChecked(True)

        self.broadcast_console_to_ops_checkbox = QCheckBox()
        self.broadcast_console_to_ops_checkbox.setChecked(True)

        self.broadcast_rcon_to_ops_checkbox = QCheckBox()
        self.broadcast_rcon_to_ops_checkbox.setChecked(True)

        self.difficulity_combobox = ComboBox()
        self.difficulity_combobox.addItems(['Peaceful', 'Easy', 'Normal', 'Hard'])
        self.difficulity_combobox.setCurrentIndex(1)

        self.enable_command_block_checkbox = QCheckBox()
        self.enable_command_block_checkbox.setChecked(False)

        self.enable_jmx_monitoring_checkbox = QCheckBox()
        self.enable_jmx_monitoring_checkbox.setChecked(False)

        self.enable_query_checkbox = QCheckBox()
        self.enable_query_checkbox.setChecked(False)

        self.enable_rcon_checkbox = QCheckBox()
        self.enable_rcon_checkbox.setChecked(False)

        self.enable_status_checkbox = QCheckBox()
        self.enable_status_checkbox.setChecked(True)

        self.enforce_secure_profile_checkbox = QCheckBox()
        self.enforce_secure_profile_checkbox.setChecked(True)

        self.enforce_whitelist_checkbox = QCheckBox()
        self.enforce_whitelist_checkbox.setChecked(False)

        self.entity_broadcast_range_percentage_spinbox = SpinBox()
        self.entity_broadcast_range_percentage_spinbox.setRange(10, 100)
        self.entity_broadcast_range_percentage_spinbox.setValue(100)

        self.force_gamemode_checkbox = QCheckBox()
        self.force_gamemode_checkbox.setChecked(False)

        self.function_permission_level_spinbox = SpinBox()
        self.function_permission_level_spinbox.setRange(1, 4)
        self.function_permission_level_spinbox.setValue(2)

        self.gamemode_combobox = ComboBox()
        self.gamemode_combobox.addItems(['Survival', 'Creative', 'Adventure', 'Spectator'])

        self.generate_structures_checkbox = QCheckBox()
        self.generate_structures_checkbox.setChecked(True)

        self.generator_settings_lineedit = QLineEdit()
        self.generator_settings_lineedit.setText('{}')

        self.hardcore_checkbox = QCheckBox()
        self.hardcore_checkbox.setChecked(False)

        self.hide_online_players_checkbox = QCheckBox()
        self.hide_online_players_checkbox.setChecked(False)

        self.initial_disabled_packs_lineedit = QLineEdit()
        self.initial_disabled_packs_lineedit.setText('')

        self.initial_enabled_packs_lineedit = QLineEdit()
        self.initial_enabled_packs_lineedit.setText('vanilla')

        self.level_name_lineedit = QLineEdit()
        self.level_name_lineedit.setText('world')

        self.level_seed_lineedit = QLineEdit()
        self.level_seed_lineedit.setText('')

        self.level_type_lineedit = QLineEdit()
        self.level_type_lineedit.setText('minecraft\:normal')

        self.max_chained_neighbor_updates_spinbox = SpinBox()
        self.max_chained_neighbor_updates_spinbox.setRange(-2147483648, 2147483647)
        self.max_chained_neighbor_updates_spinbox.setValue(1000000)

        self.max_players_spinbox = SpinBox()
        self.max_players_spinbox.setRange(0, 2147483647)
        self.max_players_spinbox.setValue(20)

        self.max_tick_time_spinbox = SpinBox()
        self.max_tick_time_spinbox.setRange(-1, 2147483647)
        self.max_tick_time_spinbox.setValue(60000)

        self.max_world_size_spinbox = SpinBox()
        self.max_world_size_spinbox.setRange(1, 29999984)
        self.max_world_size_spinbox.setValue(29999984)

        self.motd_lineedit = QLineEdit()
        self.motd_lineedit.setMaxLength(59)
        self.motd_lineedit.setText('A Minecraft Server')

        self.network_compression_threshold_spinbox = SpinBox()
        self.network_compression_threshold_spinbox.setRange(-2147483648, 2147483647)
        self.network_compression_threshold_spinbox.setValue(256)

        self.online_mode_checkbox = QCheckBox()
        self.online_mode_checkbox.setChecked(True)
        
        self.op_permission_level_spinbox = SpinBox()
        self.op_permission_level_spinbox.setRange(0, 4)
        self.op_permission_level_spinbox.setValue(4)

        self.player_idle_timeout_spinbox = SpinBox()
        self.player_idle_timeout_spinbox.setRange(0, 2147483647)
        self.player_idle_timeout_spinbox.setValue(0)

        self.prevent_proxy_connections_checkbox = QCheckBox()
        self.prevent_proxy_connections_checkbox.setChecked(False)

        self.pvp_checkbox = QCheckBox()
        self.pvp_checkbox.setChecked(True)

        self.query_port_spinbox = SpinBox()
        self.query_port_spinbox.setRange(1, 2**16-2)
        self.query_port_spinbox.setValue(25565)

        self.rate_limit_spinbox = SpinBox()
        self.rate_limit_spinbox.setRange(0, 2147483647)
        self.rate_limit_spinbox.setValue(0)

        self.rcon_password_lineedit = QLineEdit()
        self.rcon_password_lineedit.setText('')

        self.rcon_port_spinbox = SpinBox()
        self.rcon_port_spinbox.setRange(1, 2**16-2)
        self.rcon_port_spinbox.setValue(25575)

        self.resource_pack_lineedit = QLineEdit()
        self.resource_pack_lineedit.setText('')

        self.resource_pack_prompt_lineedit = QLineEdit()
        self.resource_pack_prompt_lineedit.setText('')

        self.resource_pack_sha1_lineedit = QLineEdit()
        self.resource_pack_sha1_lineedit.setText('')

        self.require_resource_pack_checkbox = QCheckBox()
        self.require_resource_pack_checkbox.setChecked(False)

        self.server_ip_lineedit = QLineEdit()
        self.server_ip_lineedit.setText('')

        self.server_port_spinbox = SpinBox()
        self.server_port_spinbox.setRange(1, 2**16-2)
        self.server_port_spinbox.setValue(25565)

        self.simulation_distance_spinbox = SpinBox()
        self.simulation_distance_spinbox.setRange(3, 32)
        self.simulation_distance_spinbox.setValue(10)

        self.spawn_animals_checkbox = QCheckBox()
        self.spawn_animals_checkbox.setChecked(True)

        self.spawn_monsters_checkbox = QCheckBox()
        self.spawn_monsters_checkbox.setChecked(True)

        self.spawn_npcs_checkbox = QCheckBox()
        self.spawn_npcs_checkbox.setChecked(True)

        self.spawn_protection_spinbox = SpinBox()
        self.spawn_protection_spinbox.setRange(0, 2147483647)
        self.spawn_protection_spinbox.setValue(16)

        self.sync_chunk_writes_checkbox = QCheckBox()
        self.sync_chunk_writes_checkbox.setChecked(True)

        self.text_filtering_config_lineedit = QLineEdit()
        self.text_filtering_config_lineedit.setText('')

        self.use_native_transport_checkbox = QCheckBox()
        self.use_native_transport_checkbox.setChecked(True)

        self.view_distance_spinbox = SpinBox()
        self.view_distance_spinbox.setRange(3, 32)
        self.view_distance_spinbox.setValue(10)

        self.white_list_checkbox = QCheckBox()
        self.white_list_checkbox.setChecked(False)

        form_layout.addRow("Allow flight", self.allow_flight_checkbox)
        form_layout.addRow("Allow nether", self.allow_nether_checkbox)
        form_layout.addRow("Broadcast console to ops", self.broadcast_console_to_ops_checkbox)
        form_layout.addRow("Broadcast RCON to ops", self.broadcast_rcon_to_ops_checkbox)
        form_layout.addRow("Difficulity", self.difficulity_combobox)
        form_layout.addRow("Enable command blocks", self.enable_command_block_checkbox)
        form_layout.addRow("Enable JMX monitoring", self.enable_jmx_monitoring_checkbox) # need to add some flags to startup
        form_layout.addRow("Enable query", self.enable_query_checkbox)
        form_layout.addRow("Enable RCON", self.enable_rcon_checkbox)
        form_layout.addRow("Enable status", self.enable_status_checkbox)
        form_layout.addRow("Enforce secure profile", self.enforce_secure_profile_checkbox)
        form_layout.addRow("Enforce whitelist", self.enforce_whitelist_checkbox)
        form_layout.addRow("Entity broadcast range percentage", self.entity_broadcast_range_percentage_spinbox)
        form_layout.addRow("Force gamemode", self.force_gamemode_checkbox)
        form_layout.addRow("Function permission level", self.function_permission_level_spinbox)
        form_layout.addRow("Gamemode", self.gamemode_combobox)
        form_layout.addRow("Generate structures", self.generate_structures_checkbox)
        form_layout.addRow("Generator settings", self.generator_settings_lineedit)
        form_layout.addRow("Hardcore", self.hardcore_checkbox)
        form_layout.addRow("Hide online players", self.hide_online_players_checkbox)
        form_layout.addRow("Initial disabled packs", self.initial_disabled_packs_lineedit)
        form_layout.addRow("Initial enabbled packs", self.initial_enabled_packs_lineedit)
        form_layout.addRow("Level name", self.level_name_lineedit)
        form_layout.addRow("Level seed", self.level_seed_lineedit)
        form_layout.addRow("Level type", self.level_type_lineedit)
        form_layout.addRow("Max chained neighbor updates", self.max_chained_neighbor_updates_spinbox)
        form_layout.addRow("Max players", self.max_players_spinbox)
        form_layout.addRow("Max tick time", self.max_tick_time_spinbox)
        form_layout.addRow("Max world size", self.max_world_size_spinbox)
        form_layout.addRow("MOTD", self.motd_lineedit)
        form_layout.addRow("Network compression threshold", self.network_compression_threshold_spinbox)
        form_layout.addRow("Online mode", self.online_mode_checkbox)
        form_layout.addRow("OP permission level", self.op_permission_level_spinbox)
        form_layout.addRow("Player idle timeout", self.player_idle_timeout_spinbox)
        form_layout.addRow("Prevent proxy connections", self.prevent_proxy_connections_checkbox)
        form_layout.addRow("PVP", self.pvp_checkbox)
        form_layout.addRow("Query port", self.query_port_spinbox)
        form_layout.addRow("Rate limit", self.rate_limit_spinbox)
        form_layout.addRow("RCON password", self.rcon_password_lineedit)
        form_layout.addRow("RCON port", self.rcon_port_spinbox)
        form_layout.addRow("Resource pack", self.resource_pack_lineedit)
        form_layout.addRow("Resource pack prompt", self.resource_pack_prompt_lineedit)
        form_layout.addRow("Resource pack SHA-1", self.resource_pack_sha1_lineedit)
        form_layout.addRow("Require resource pack", self.require_resource_pack_checkbox)
        form_layout.addRow("Server IP", self.server_ip_lineedit)
        form_layout.addRow("Server port", self.server_port_spinbox)
        form_layout.addRow("Simulation distance", self.simulation_distance_spinbox)
        form_layout.addRow("Spawn animals", self.spawn_animals_checkbox)
        form_layout.addRow("Spawn monsters", self.spawn_monsters_checkbox)
        form_layout.addRow("Spawn NPCs", self.spawn_npcs_checkbox)
        form_layout.addRow("Spawn protection", self.spawn_protection_spinbox)
        form_layout.addRow("Sync chunk writes", self.sync_chunk_writes_checkbox)
        form_layout.addRow("Text filtering config", self.text_filtering_config_lineedit)
        form_layout.addRow("Use native transport", self.use_native_transport_checkbox)
        form_layout.addRow("View distance", self.view_distance_spinbox)
        form_layout.addRow("Whitelist", self.white_list_checkbox)

        container_widget = QWidget()
        container_widget.setLayout(form_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(container_widget)
        scroll_area.setWidgetResizable(True)

        return scroll_area

    def create_settings_layout(self):
        form_layout = QFormLayout()
        server_settings = get_default_settings()

        # version = self.version_select.currentText()

        # create widgets for each setting
        self.Xmx_spinbox = QSpinBox()
        self.Xmx_spinbox.setRange(0, 2147483647)
        self.Xmx_spinbox.setValue(server_settings['_Xmx'])
        self.Xms_spinbox = QSpinBox()
        self.Xms_spinbox.setRange(0, 2147483647)
        self.Xms_spinbox.setValue(server_settings['_Xms'])
        self.bonus_chest_checkbox = QCheckBox()
        self.bonus_chest_checkbox.setChecked(server_settings['_bonusChest'])
        self.erase_cache_checkbox = QCheckBox()
        self.erase_cache_checkbox.setChecked(server_settings['_eraseCache'])
        self.force_upgrade_checkbox = QCheckBox()
        self.force_upgrade_checkbox.setChecked(server_settings['_forceUpgrade'])
        # self.initSettings_checkbox = QCheckBox()
        # self.initSettings_checkbox.setChecked(server_settings['_initSettings'])
        # self.port_spinbox = QSpinBox()
        # self.port_spinbox.setRange(0, 65536)
        # self.port_spinbox.setValue(server_settings['_port'])
        self.safe_mode_checkbox = QCheckBox()
        self.safe_mode_checkbox.setChecked(server_settings['_safeMode'])
        self.universe_lineedit = QLineEdit()
        self.universe_lineedit.setText(server_settings['_universe'])
        # self.world_lineedit = QLineEdit()
        # self.world_lineedit.setText(server_settings['_world'])

        # add widgets to form layout
        form_layout.addRow("Xmx (MB)", self.Xmx_spinbox)
        form_layout.addRow("Xms (MB)", self.Xms_spinbox)
        form_layout.addRow("Generate bonus chest", self.bonus_chest_checkbox)
        form_layout.addRow("Erase cache", self.erase_cache_checkbox)
        form_layout.addRow("Force upgrade", self.force_upgrade_checkbox)
        # form_layout.addRow("Load settings from file", self.initSettings_checkbox)
        # form_layout.addRow("Port", self.port_spinbox)
        form_layout.addRow("Load level with vanilla datapack only", self.safe_mode_checkbox)
        form_layout.addRow("Universe folder", self.universe_lineedit)
        # form_layout.addRow("World folder", self.world_lineedit)

        return form_layout

    def refresh(self):
        self.servers = get_servers(self.settings.data_location)
        self.servers_selection.refresh(self.servers)
        print('refresh servers')

    def create_server(self):
        settings, properties = self.get_server_values()
        version = settings['version']

        server_data_path = os.path.join(self.settings.data_location, settings['name'])

        if os.path.exists(server_data_path):
            raise Exception("Server data path already exists") # TODO

        os.makedirs(server_data_path)
        jar_path = downloader.download_server_jar(version, server_data_path)

        server_settings = ServerSettings()
        self.set_server_settings(server_settings, settings)
        server = Server(server_data_path, server_settings, jar_path)

        start_server(self.thread_handler, [server], 0)
        # TODO eula, server.properties

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

class SpinBox(QSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class ComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()
