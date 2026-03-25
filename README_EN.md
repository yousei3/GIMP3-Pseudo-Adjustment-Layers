# Pseudo Adjustment Layer for GIMP 3

**Pseudo Adjustment Layer** is a Python plug-in that leverages the new Non-Destructive Editing (NDE) features in GIMP 3.0/3.2 to simulate "Adjustment Layers", a familiar and essential feature in image editors like Photoshop.

It allows you to easily add, manage, and re-edit non-destructive filters from a dedicated palette without directly altering the original pixels of your image.

## ✨ Key Features

* **Automatic Pseudo Adjustment Layer Generation**: Selecting a filter automatically creates a Layer Group with a transparent dummy layer inside, and applies the non-destructive filter to the group itself.
* **Automatic Selection Masking**: If a selection exists when applying a filter, it is automatically converted into a Layer Mask for the group.
* **Perfect Match with GIMP Menus**: Displays over 100 GEGL filters in the exact same categories and order as GIMP's official `Filters` menu.
* **Powerful Management Tools**: 
    * 🔍 Real-time incremental search.
    * ⭐ Favorites system (right-click to add/remove).
    * 📝 History of recently used filters (up to 10).
    * 📂 Clean, accordion-style exclusive folder expansion.
* **Fully Customisable Multilingual Support**: When you select a language in the plug-in, a JSON file for that language is automatically generated in the `Language` folder. You can freely change any UI display names by editing this file.
* **Safe Validation**: Clicking the **`Reset List`** button at the bottom of the palette not only reloads the list but also automatically tests internal GEGL nodes. It safely excludes any nodes that do not function correctly as non-destructive filters.

## ⚙️ How it Works

In the current specification of GIMP 3, it is not possible to apply a filter directly to an empty layer.
This plug-in achieves the behaviour of an adjustment layer by executing the following steps instantly in the background:

1. Creates a new Layer Group (named `fx: Filter Name`) directly above the currently selected layer.
2. Places a transparent layer (named `DUMMY`) inside the group.
3. Adds a Layer Mask to the group (if a selection is active).
4. Applies the specified non-destructive filter to the Layer Group itself.

This workflow allows you to adjust parameters, toggle visibility, or repaint the mask at any time later.

## 📦 Installation

1. Download and extract `pseudo_adjustment_layers.zip`.
2. Place the extracted folder in your GIMP 3 plug-ins directory:
   * **Linux**: `~/.config/GIMP/3.0/plug-ins/`
   * **Windows**: `C:\Users\[Username]\AppData\Roaming\GIMP\3.0\plug-ins\`

   Make sure the folder structure looks like this:

       plug-ins/
          └── pseudo_adjustment_layers/
                   └── pseudo_adjustment_layers.py

3. Grant execution permissions to the file.
   * On Linux, run: `chmod +x pseudo_adjustment_layers.py` in your terminal.
4. Restart GIMP.

## 🚀 Usage

1. Launch the palette from the GIMP menu: **`Filters` > `Pseudo Adjustment Layer`**. (The palette stays on top of the GIMP window).
   > **NOTE**: On first startup, please click the **`🔄 Reset List`** button at the bottom of the palette to initialize the filter list.
2. Select the target layer in your image to which you want to apply the filter.
3. **Double-click** (or press Enter on) a filter name in the palette to apply it as a pseudo adjustment layer above the selected layer.

### Customising the UI
When you choose a language via the `🌐 Select` button, a `Language` folder is created next to the plug-in, containing a `(language_code).json` file (e.g., `ja.json` or `en_GB.json`).
By opening this JSON file in a text editor and modifying the `"local"` values, you can customise the category and filter names displayed in the palette to your liking. After editing, click the button at the bottom of the palette to validate and reload your custom translations.

## ⚠️ Requirements
* GIMP 3.0 or 3.2+
* Python 3 environment with GObject Introspection (GIR) support

## 📜 License
This project is open source and available under the [GNU General Public License v3.0 (GPLv3)](LICENSE).