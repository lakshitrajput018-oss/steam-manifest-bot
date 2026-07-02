-- Meccha Chameleon Lua Manifest Configuration
local manifest = {
    app_id = "4704690",
    app_name = "Meccha Chameleon",
    version = "1.0.0",
    depots = {
        {
            id = "4704691",
            name = "Base Game",
            manifest_id = "1234567890"
        }
    },
    install_path = "common/meccha_chameleon",
    created_at = os.time(),
    updated_at = os.time()
}

return manifest
