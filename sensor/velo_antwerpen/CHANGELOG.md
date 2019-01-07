# 1.2.0

- Use show_on_map config option to display the station on map and show the Velo logo

# 1.1.0

- Provide a lot more attributes. Attributes will now look like the example below. 914109dff0a59794f47e8a69e55c152c4add993b

```py
self.attributes = {
    'available_slots': 20,
    'latitude': "51.248223",
    'longitude': "4.444239",
    "station_address": "Speelpleinstraat \/ Terlindenhofstraat",
    "station_id": 23,
    "station_name": "Speelplein",
    "station_opened": True,
    ATTR_ATTRIBUTION: "https://www.velo-antwerpen.be/",
}
```

- Cleanup component code 35f6d30f5e168b57637684142971fdc4e2d7f9e8

# 1.0.0

- Implement support for [custom_updater](https://github.com/custom-components/custom_updater)
