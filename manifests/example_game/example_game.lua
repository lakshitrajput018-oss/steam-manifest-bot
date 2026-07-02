-- Example Lua Manifest Configuration
-- Replace this with your actual Lua configuration

local manifest = {
    app_id = "123456",
    app_name = "Example Game",
    version = "1.0.0",
    
    -- Depot information
    depots = {
        {
            id = "123457",
            name = "Base Game",
            manifest_id = "1234567890123456"
        }
    },
    
    -- Installation paths
    install_path = "common/example_game",
    
    -- Metadata
    created_at = os.time(),
    updated_at = os.time()
}

return manifest
