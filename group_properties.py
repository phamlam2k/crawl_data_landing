import json
from collections import defaultdict

def group_properties():
    # Load the properties data from all_properties.json
    with open('all_properties.json', 'r', encoding='utf-8') as file:
        properties = json.load(file)

    # Group properties by location and road, and calculate the average price per m²
    grouped_properties = defaultdict(lambda: {'roads': defaultdict(lambda: {'properties': [], 'total_price_per_m2': 0, 'count': 0}),
                                              'total_price_per_m2': 0, 'count': 0})

    for property in properties:
        location = property.get('location', '').strip()
        road = property.get('road', '').strip()

        if location and location not in ["", "·", "N/A"]:  # Exclude unwanted locations
            price_per_m2 = property.get('price_per_m2', '').strip()  # Ensure we get a string
            valid_price_per_m2 = False  # Flag to check if price_per_m2 is valid

            if price_per_m2 and price_per_m2 != "N/A":  # Check if price_per_m2 is valid
                try:
                    price_per_m2_value = float(price_per_m2.replace(' tr/m²', '').replace(',', '.').strip())
                    valid_price_per_m2 = True  # Mark as valid if conversion is successful
                except ValueError:
                    price_per_m2_value = 0  # Default to 0 if conversion fails
            else:  # Calculate price_per_m2 using price and area
                price = property.get('price', '0 tỷ').replace(' tỷ', '').replace(',', '.')
                area = property.get('area', '0 m²').replace(' m²', '').replace(',', '.')
                try:
                    if price and area:  # Ensure both values exist
                        price_value = float(price) * 1000  # Convert tỷ to VNĐ
                        area_value = float(area)  # m²
                        price_per_m2_value = price_value / area_value
                        valid_price_per_m2 = True  # Mark as valid if calculation is successful
                    else:
                        price_per_m2_value = 0
                except (ValueError, ZeroDivisionError):
                    price_per_m2_value = 0

            # Update grouped properties if we have a valid price per m²
            if valid_price_per_m2:
                property['price_per_m2_value'] = round(price_per_m2_value, 1)  # Round to 1 decimal place

                # Update the road level group
                grouped_properties[location]['roads'][road]['properties'].append(property)
                grouped_properties[location]['roads'][road]['total_price_per_m2'] += price_per_m2_value
                grouped_properties[location]['roads'][road]['count'] += 1

                # Update the location level group
                grouped_properties[location]['total_price_per_m2'] += price_per_m2_value
                grouped_properties[location]['count'] += 1
            else:
                property['price_per_m2_value'] = round(price_per_m2_value, 1)
                grouped_properties[location]['roads'][road]['properties'].append(property)

    # Calculate the average price per m² for each road and location
    for location, loc_data in grouped_properties.items():
        for road, road_data in loc_data['roads'].items():
            if road_data['count'] > 0:
                road_data['average_price_per_m2'] = round(road_data['total_price_per_m2'] / road_data['count'], 1)
            else:
                road_data['average_price_per_m2'] = 0

        if loc_data['count'] > 0:
            loc_data['average_price_per_m2'] = round(loc_data['total_price_per_m2'] / loc_data['count'], 1)
        else:
            loc_data['average_price_per_m2'] = 0

    # Convert grouped properties to a regular dict for JSON serialization
    grouped_properties_dict = {
        location: {
            'roads': {
                road: {
                    'properties': road_data['properties'],
                    'average_price_per_m2': road_data['average_price_per_m2']
                } for road, road_data in loc_data['roads'].items()
            },
            'average_price_per_m2': loc_data['average_price_per_m2']
        } for location, loc_data in grouped_properties.items()
    }

    # Save the grouped properties to a new JSON file
    with open('grouped_properties.json', 'w', encoding='utf-8') as file:
        json.dump(grouped_properties_dict, file, ensure_ascii=False, indent=4)

    print("Properties grouped by location and road with average price per m² saved to grouped_properties.json")



# Example usage
if __name__ == "__main__":
    group_properties()
