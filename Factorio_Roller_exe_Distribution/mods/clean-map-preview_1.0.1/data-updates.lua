for _, elem in pairs(data.raw["tile"]) do
    elem.map_color = {r=127, g=90, b=54}
end
data.raw["tile"]["deepwater"].map_color = {r=45, g=94, b=127}
data.raw["tile"]["water"].map_color = {r=45, g=94, b=127}
data.raw["tile"]["water-shallow"].map_color = {r=45, g=94, b=127}
data.raw["tile"]["deepwater-green"].map_color = {r=45, g=94, b=127}
data.raw["tile"]["water-green"].map_color = {r=45, g=94, b=127}
data.raw["tile"]["water-mud"].map_color = {r=45, g=94, b=127}
for _, elem in pairs(data.raw["resource"]) do
    elem.map_grid = false
end
data.raw["resource"]["coal"].map_color = {r=30, g=30, b=30}
data.raw["resource"]["iron-ore"].map_color = {r=0, g=229, b=229}
data.raw["resource"]["copper-ore"].map_color = {r=255, g=127, b=0}
data.raw["resource"]["crude-oil"].map_color = {r=255, g=0, b=255}
data.raw["resource"]["stone"].map_color = {r=255, g=255, b=0}
data.raw["simple-entity"]["rock-huge"].flags = {"placeable-neutral", "placeable-off-grid"}
data.raw["simple-entity"]["rock-huge"].map_color = {r=255, g=255, b=0}
for _, elem in pairs(data.raw["tree"]) do
    elem.map_color = {r=64, g=64, b=0}
end


