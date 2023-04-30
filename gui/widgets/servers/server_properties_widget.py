from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QCheckBox,
    QLineEdit,
    QGroupBox,
    QScrollArea
)

from minecraft_server import server_properties
from gui.widgets.combo_box import ComboBox
from gui.widgets.spin_box import SpinBox


class ServerPropertiesWidget(QWidget):
    def __init__(self, server_path=None, parent=None):
        super().__init__()

        self.server_path = server_path
        self._get_server_properties()
        self.create_config_layout()

        self.config_group = QGroupBox("Server configuration")
        self.config_group.setLayout(QVBoxLayout())
        self.config_group.layout().addWidget(self.config_scroll_area)

        layout = QVBoxLayout()
        layout.addWidget(self.config_group)
        self.setLayout(layout)


    def _get_server_properties(self):
        if self.server_path:
            self.server_properties = server_properties.read(self.server_path)
        else:
            self.server_properties = server_properties.get_default_server_properties()
            self.server_properties = server_properties.unstringify(self.server_properties)


    def create_config_layout(self):
        config_layout = QFormLayout()

        self.allow_flight_checkbox = QCheckBox()
        self.allow_flight_checkbox.setChecked(self.server_properties['allow-flight'])

        self.allow_nether_checkbox = QCheckBox()
        self.allow_nether_checkbox.setChecked(self.server_properties['allow-nether'])

        self.broadcast_console_to_ops_checkbox = QCheckBox()
        self.broadcast_console_to_ops_checkbox.setChecked(self.server_properties['broadcast-console-to-ops'])

        self.broadcast_rcon_to_ops_checkbox = QCheckBox()
        self.broadcast_rcon_to_ops_checkbox.setChecked(self.server_properties['broadcast-rcon-to-ops'])

        self.difficulity_combobox = ComboBox()
        self.difficulity_combobox.addItems(['Peaceful', 'Easy', 'Normal', 'Hard'])
        self.difficulity_combobox.setCurrentText(self.server_properties['difficulty'])

        self.enable_command_block_checkbox = QCheckBox()
        self.enable_command_block_checkbox.setChecked(self.server_properties['enable-command-block'])

        self.enable_jmx_monitoring_checkbox = QCheckBox()
        self.enable_jmx_monitoring_checkbox.setChecked(self.server_properties['enable-jmx-monitoring'])

        self.enable_query_checkbox = QCheckBox()
        self.enable_query_checkbox.setChecked(self.server_properties['enable-query'])

        self.enable_rcon_checkbox = QCheckBox()
        self.enable_rcon_checkbox.setChecked(self.server_properties['enable-rcon'])

        self.enable_status_checkbox = QCheckBox()
        self.enable_status_checkbox.setChecked(self.server_properties['enable-status'])

        self.enforce_secure_profile_checkbox = QCheckBox()
        self.enforce_secure_profile_checkbox.setChecked(self.server_properties['enforce-secure-profile'])

        self.enforce_whitelist_checkbox = QCheckBox()
        self.enforce_whitelist_checkbox.setChecked(self.server_properties['enforce-whitelist'])

        self.entity_broadcast_range_percentage_spinbox = SpinBox()
        self.entity_broadcast_range_percentage_spinbox.setRange(10, 100)
        self.entity_broadcast_range_percentage_spinbox.setValue(self.server_properties['entity-broadcast-range-percentage'])

        self.force_gamemode_checkbox = QCheckBox()
        self.force_gamemode_checkbox.setChecked(self.server_properties['force-gamemode'])

        self.function_permission_level_spinbox = SpinBox()
        self.function_permission_level_spinbox.setRange(1, 4)
        self.function_permission_level_spinbox.setValue(self.server_properties['function-permission-level'])

        self.gamemode_combobox = ComboBox()
        self.gamemode_combobox.addItems(['Survival', 'Creative', 'Adventure', 'Spectator'])
        self.gamemode_combobox.setCurrentText(self.server_properties['gamemode'])

        self.generate_structures_checkbox = QCheckBox()
        self.generate_structures_checkbox.setChecked(self.server_properties['generate-structures'])

        self.generator_settings_lineedit = QLineEdit()
        self.generator_settings_lineedit.setText(self.server_properties['generator-settings'])

        self.hardcore_checkbox = QCheckBox()
        self.hardcore_checkbox.setChecked(self.server_properties['hardcore'])

        self.hide_online_players_checkbox = QCheckBox()
        self.hide_online_players_checkbox.setChecked(self.server_properties['hide-online-players'])

        self.initial_disabled_packs_lineedit = QLineEdit()
        self.initial_disabled_packs_lineedit.setText(self.server_properties['initial-disabled-packs'])

        self.initial_enabled_packs_lineedit = QLineEdit()
        self.initial_enabled_packs_lineedit.setText(self.server_properties['initial-enabled-packs'])

        self.level_name_lineedit = QLineEdit()
        self.level_name_lineedit.setText(self.server_properties['level-name'])

        self.level_seed_lineedit = QLineEdit()
        self.level_seed_lineedit.setText(self.server_properties['level-seed'])

        self.level_type_lineedit = QLineEdit()
        self.level_type_lineedit.setText(self.server_properties['level-type'])

        self.max_chained_neighbor_updates_spinbox = SpinBox()
        self.max_chained_neighbor_updates_spinbox.setRange(-2147483648, 2147483647)
        self.max_chained_neighbor_updates_spinbox.setValue(self.server_properties['max-chained-neighbor-updates'])

        self.max_players_spinbox = SpinBox()
        self.max_players_spinbox.setRange(0, 2147483647)
        self.max_players_spinbox.setValue(self.server_properties['max-players'])

        self.max_tick_time_spinbox = SpinBox()
        self.max_tick_time_spinbox.setRange(-1, 2147483647)
        self.max_tick_time_spinbox.setValue(self.server_properties['max-tick-time'])

        self.max_world_size_spinbox = SpinBox()
        self.max_world_size_spinbox.setRange(1, 29999984)
        self.max_world_size_spinbox.setValue(self.server_properties['max-world-size'])

        self.motd_lineedit = QLineEdit()
        self.motd_lineedit.setMaxLength(59)
        self.motd_lineedit.setText(self.server_properties['motd'])

        self.network_compression_threshold_spinbox = SpinBox()
        self.network_compression_threshold_spinbox.setRange(-2147483648, 2147483647)
        self.network_compression_threshold_spinbox.setValue(self.server_properties['network-compression-threshold'])

        self.online_mode_checkbox = QCheckBox()
        self.online_mode_checkbox.setChecked(self.server_properties['online-mode'])
        
        self.op_permission_level_spinbox = SpinBox()
        self.op_permission_level_spinbox.setRange(0, 4)
        self.op_permission_level_spinbox.setValue(self.server_properties['op-permission-level'])

        self.player_idle_timeout_spinbox = SpinBox()
        self.player_idle_timeout_spinbox.setRange(0, 2147483647)
        self.player_idle_timeout_spinbox.setValue(self.server_properties['player-idle-timeout'])

        self.prevent_proxy_connections_checkbox = QCheckBox()
        self.prevent_proxy_connections_checkbox.setChecked(self.server_properties['prevent-proxy-connections'])

        self.pvp_checkbox = QCheckBox()
        self.pvp_checkbox.setChecked(self.server_properties['pvp'])

        self.query_port_spinbox = SpinBox()
        self.query_port_spinbox.setRange(1, 65534)
        self.query_port_spinbox.setValue(self.server_properties['query.port'])

        self.rate_limit_spinbox = SpinBox()
        self.rate_limit_spinbox.setRange(0, 2147483647)
        self.rate_limit_spinbox.setValue(self.server_properties['rate-limit'])

        self.rcon_password_lineedit = QLineEdit()
        self.rcon_password_lineedit.setText(self.server_properties['rcon.password'])

        self.rcon_port_spinbox = SpinBox()
        self.rcon_port_spinbox.setRange(1, 65534)
        self.rcon_port_spinbox.setValue(self.server_properties['rcon.port'])

        self.require_resource_pack_checkbox = QCheckBox()
        self.require_resource_pack_checkbox.setChecked(self.server_properties['require-resource-pack'])

        self.resource_pack_lineedit = QLineEdit()
        self.resource_pack_lineedit.setText(self.server_properties['resource-pack'])

        self.resource_pack_prompt_lineedit = QLineEdit()
        self.resource_pack_prompt_lineedit.setText(self.server_properties['resource-pack-prompt'])

        self.resource_pack_sha1_lineedit = QLineEdit()
        self.resource_pack_sha1_lineedit.setText(self.server_properties['resource-pack-sha1'])

        self.server_ip_lineedit = QLineEdit()
        self.server_ip_lineedit.setText(self.server_properties['server-ip'])

        self.server_port_spinbox = SpinBox()
        self.server_port_spinbox.setRange(1, 65534)
        self.server_port_spinbox.setValue(self.server_properties['server-port'])

        self.simulation_distance_spinbox = SpinBox()
        self.simulation_distance_spinbox.setRange(3, 32)
        self.simulation_distance_spinbox.setValue(self.server_properties['simulation-distance'])

        self.spawn_animals_checkbox = QCheckBox()
        self.spawn_animals_checkbox.setChecked(self.server_properties['spawn-animals'])

        self.spawn_monsters_checkbox = QCheckBox()
        self.spawn_monsters_checkbox.setChecked(self.server_properties['spawn-monsters'])

        self.spawn_npcs_checkbox = QCheckBox()
        self.spawn_npcs_checkbox.setChecked(self.server_properties['spawn-npcs'])

        self.spawn_protection_spinbox = SpinBox()
        self.spawn_protection_spinbox.setRange(0, 2147483647)
        self.spawn_protection_spinbox.setValue(self.server_properties['spawn-protection'])

        self.sync_chunk_writes_checkbox = QCheckBox()
        self.sync_chunk_writes_checkbox.setChecked(self.server_properties['sync-chunk-writes'])

        self.text_filtering_config_lineedit = QLineEdit()
        self.text_filtering_config_lineedit.setText(self.server_properties['text-filtering-config'])

        self.use_native_transport_checkbox = QCheckBox()
        self.use_native_transport_checkbox.setChecked(self.server_properties['use-native-transport'])

        self.view_distance_spinbox = SpinBox()
        self.view_distance_spinbox.setRange(3, 32)
        self.view_distance_spinbox.setValue(self.server_properties['view-distance'])

        self.white_list_checkbox = QCheckBox()
        self.white_list_checkbox.setChecked(self.server_properties['white-list'])

        config_layout.addRow("Allow flight", self.allow_flight_checkbox)
        config_layout.addRow("Allow nether", self.allow_nether_checkbox)
        config_layout.addRow("Broadcast console to ops", self.broadcast_console_to_ops_checkbox)
        config_layout.addRow("Broadcast RCON to ops", self.broadcast_rcon_to_ops_checkbox)
        config_layout.addRow("Difficulity", self.difficulity_combobox)
        config_layout.addRow("Enable command blocks", self.enable_command_block_checkbox)
        config_layout.addRow("Enable JMX monitoring", self.enable_jmx_monitoring_checkbox) # need to add some flags to startup
        config_layout.addRow("Enable query", self.enable_query_checkbox)
        config_layout.addRow("Enable RCON", self.enable_rcon_checkbox)
        config_layout.addRow("Enable status", self.enable_status_checkbox)
        config_layout.addRow("Enforce secure profile", self.enforce_secure_profile_checkbox)
        config_layout.addRow("Enforce whitelist", self.enforce_whitelist_checkbox)
        config_layout.addRow("Entity broadcast range percentage", self.entity_broadcast_range_percentage_spinbox)
        config_layout.addRow("Force gamemode", self.force_gamemode_checkbox)
        config_layout.addRow("Function permission level", self.function_permission_level_spinbox)
        config_layout.addRow("Gamemode", self.gamemode_combobox)
        config_layout.addRow("Generate structures", self.generate_structures_checkbox)
        config_layout.addRow("Generator settings", self.generator_settings_lineedit)
        config_layout.addRow("Hardcore", self.hardcore_checkbox)
        config_layout.addRow("Hide online players", self.hide_online_players_checkbox)
        config_layout.addRow("Initial disabled packs", self.initial_disabled_packs_lineedit)
        config_layout.addRow("Initial enabbled packs", self.initial_enabled_packs_lineedit)
        config_layout.addRow("Level name", self.level_name_lineedit)
        config_layout.addRow("Level seed", self.level_seed_lineedit)
        config_layout.addRow("Level type", self.level_type_lineedit)
        config_layout.addRow("Max chained neighbor updates", self.max_chained_neighbor_updates_spinbox)
        config_layout.addRow("Max players", self.max_players_spinbox)
        config_layout.addRow("Max tick time", self.max_tick_time_spinbox)
        config_layout.addRow("Max world size", self.max_world_size_spinbox)
        config_layout.addRow("MOTD", self.motd_lineedit)
        config_layout.addRow("Network compression threshold", self.network_compression_threshold_spinbox)
        config_layout.addRow("Online mode", self.online_mode_checkbox)
        config_layout.addRow("OP permission level", self.op_permission_level_spinbox)
        config_layout.addRow("Player idle timeout", self.player_idle_timeout_spinbox)
        config_layout.addRow("Prevent proxy connections", self.prevent_proxy_connections_checkbox)
        config_layout.addRow("PVP", self.pvp_checkbox)
        config_layout.addRow("Query port", self.query_port_spinbox)
        config_layout.addRow("Rate limit", self.rate_limit_spinbox)
        config_layout.addRow("RCON password", self.rcon_password_lineedit)
        config_layout.addRow("RCON port", self.rcon_port_spinbox)
        config_layout.addRow("Require resource pack", self.require_resource_pack_checkbox)
        config_layout.addRow("Resource pack", self.resource_pack_lineedit)
        config_layout.addRow("Resource pack prompt", self.resource_pack_prompt_lineedit)
        config_layout.addRow("Resource pack SHA-1", self.resource_pack_sha1_lineedit)
        config_layout.addRow("Server IP", self.server_ip_lineedit)
        config_layout.addRow("Server port", self.server_port_spinbox)
        config_layout.addRow("Simulation distance", self.simulation_distance_spinbox)
        config_layout.addRow("Spawn animals", self.spawn_animals_checkbox)
        config_layout.addRow("Spawn monsters", self.spawn_monsters_checkbox)
        config_layout.addRow("Spawn NPCs", self.spawn_npcs_checkbox)
        config_layout.addRow("Spawn protection", self.spawn_protection_spinbox)
        config_layout.addRow("Sync chunk writes", self.sync_chunk_writes_checkbox)
        config_layout.addRow("Text filtering config", self.text_filtering_config_lineedit)
        config_layout.addRow("Use native transport", self.use_native_transport_checkbox)
        config_layout.addRow("View distance", self.view_distance_spinbox)
        config_layout.addRow("Whitelist", self.white_list_checkbox)

        container_widget = QWidget()
        container_widget.setLayout(config_layout)

        self.config_scroll_area = QScrollArea()
        self.config_scroll_area.setWidget(container_widget)
        self.config_scroll_area.setWidgetResizable(True)

        return self.config_scroll_area
