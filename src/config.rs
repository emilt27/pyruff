use std::path::Path;

use ruff_workspace::configuration::Configuration;
use ruff_workspace::pyproject::{find_settings_toml, find_user_settings_toml};
use ruff_workspace::resolver::{
    resolve_root_settings, ConfigurationOrigin, ConfigurationTransformer,
};
use ruff_workspace::Settings;

struct NoOpTransformer;

impl ConfigurationTransformer for NoOpTransformer {
    fn transform(&self, config: Configuration) -> Configuration {
        config
    }
}

/// Resolve ruff settings from a config file path or by auto-discovery.
///
/// - If `config_path` is Some, resolve from that specific file.
/// - If `config_path` is None, walk ancestors from `anchor` (or CWD) to find config.
/// - Returns None if no config found (caller should use defaults).
pub fn resolve_settings(
    config_path: Option<&str>,
    anchor: Option<&str>,
) -> anyhow::Result<Option<Settings>> {
    if let Some(path) = config_path {
        // Explicit config file
        let config_file = Path::new(path);
        if !config_file.exists() {
            anyhow::bail!("Config file not found: {path}");
        }
        let settings = resolve_root_settings(
            config_file,
            &NoOpTransformer,
            ConfigurationOrigin::UserSpecified,
        )?;
        return Ok(Some(settings));
    }

    // Auto-discover: walk ancestors from anchor or CWD
    let search_from = if let Some(anchor_path) = anchor {
        let p = Path::new(anchor_path);
        if p.is_file() {
            p.parent().unwrap_or(Path::new(".")).to_path_buf()
        } else {
            p.to_path_buf()
        }
    } else {
        std::env::current_dir()?
    };

    // Try to find config in ancestors
    if let Some(config_file) = find_settings_toml(&search_from)? {
        let settings = resolve_root_settings(
            &config_file,
            &NoOpTransformer,
            ConfigurationOrigin::Ancestor,
        )?;
        return Ok(Some(settings));
    }

    // Try user-level config
    if let Some(user_config) = find_user_settings_toml() {
        let settings = resolve_root_settings(
            &user_config,
            &NoOpTransformer,
            ConfigurationOrigin::UserSettings,
        )?;
        return Ok(Some(settings));
    }

    Ok(None)
}
