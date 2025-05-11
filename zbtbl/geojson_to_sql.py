import json

with open('e:/Folders/Desktop/北邮建筑.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

sql_statements = []
for feature in geojson_data['features']:
    name = feature['properties']['name']
    if name is None:
        name_str = 'NULL'
    else:
        name_str = f"'{name}'"
    feature_type = feature['geometry']['type']
    coordinates = feature['geometry']['coordinates']
    geom_wkt = ""
    if feature_type == 'Point':
        truncated_coord = [round(coord, 7) for coord in coordinates]
        geom_wkt = f"POINT({truncated_coord[0]}  {truncated_coord[1]})"
    elif feature_type == 'MultiLineString':
        line_strings = []
        for line in coordinates:
            truncated_line = [[round(coord, 7) for coord in point] for point in line]
            line_str = ', '.join([f"{point[0]} {point[1]}" for point in truncated_line])
            line_strings.append(f"({line_str})")
        geom_wkt = f"MULTILINESTRING({', '.join(line_strings)})"
    elif feature_type == 'MultiPolygon':
        polygons = []
        for polygon in coordinates:
            rings = []
            for ring in polygon:
                truncated_ring = [[round(coord, 7) for coord in point] for point in ring]
                ring_str = ', '.join([f"{point[0]} {point[1]}" for point in truncated_ring])
                rings.append(f"({ring_str})")
            polygons.append(f"({', '.join(rings)})")
        geom_wkt = f"MULTIPOLYGON({', '.join(polygons)})"

    sql = f"INSERT INTO map_feature (name, type, geom) VALUES ({name_str}, '{feature_type}', ST_GeomFromText('{geom_wkt}'));"
    sql_statements.append(sql)

for sql in sql_statements:
    print(sql)