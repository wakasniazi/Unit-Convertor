import gradio as gr

# Conversion dictionary
conversion_factors = {
    "Weight": {
        "Kilogram": 1,
        "Gram": 1000,
        "Pound": 2.20462
    },
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Foot": 3.28084,
        "Inch": 39.3701,
        "Mile": 0.000621371
    },
    "Volume": {
        "Liter": 1,
        "Milliliter": 1000,
        "Gallon": 0.264172
    },
    "Time": {
        "Second": 1,
        "Minute": 1/60,
        "Hour": 1/3600,
        "Day": 1/86400
    },
    "Area": {
        "Square Meter": 1,
        "Square Foot": 10.7639,
        "Acre": 0.000247105,
        "Hectare": 0.0001
    },
    "Speed": {
        "m/s": 1,
        "Km/h": 3.6,
        "mph": 2.23694
    }
}

# Get units for category
def update_units(category):
    units = list(conversion_factors[category].keys())
    return (
        gr.update(choices=units, value=units[0]),
        gr.update(choices=units, value=units[1])
    )

# Convert units
def convert(category, from_unit, to_unit, value):

    if value is None:
        return ""

    # Temperature
    if category == "Temperature":

        if from_unit == to_unit:
            return value

        if from_unit == "Celsius":
            c = value
        elif from_unit == "Fahrenheit":
            c = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            c = value - 273.15

        if to_unit == "Celsius":
            return round(c, 4)
        elif to_unit == "Fahrenheit":
            return round(c * 9 / 5 + 32, 4)
        elif to_unit == "Kelvin":
            return round(c + 273.15, 4)

    # Other categories
    base = value / conversion_factors[category][from_unit]
    result = base * conversion_factors[category][to_unit]

    return round(result, 6)

# Categories
categories = list(conversion_factors.keys()) + ["Temperature"]

with gr.Blocks(title="Universal Unit Converter") as demo:

    gr.Markdown("# 🌍 Universal Unit Converter")

    gr.Markdown(
        "Convert Weight, Length, Temperature, Area, Volume, Time and Speed."
    )

    category = gr.Dropdown(
        categories,
        value="Weight",
        label="Category"
    )

    from_unit = gr.Dropdown(label="From Unit")

    to_unit = gr.Dropdown(label="To Unit")

    value = gr.Number(label="Enter Value")

    output = gr.Number(label="Converted Value")

    convert_btn = gr.Button("Convert")

    category.change(
        update_units,
        category,
        [from_unit, to_unit]
    )

    convert_btn.click(
        convert,
        [category, from_unit, to_unit, value],
        output
    )

    demo.load(
        update_units,
        category,
        [from_unit, to_unit]
    )

demo.launch()
