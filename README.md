# DayZ-LOD-Tools Addon for Blender

Welcome to **DayZ-LOD-Tools**, an addon for Blender designed to streamline the creation of Level of Detail (LOD) models for use with Arma 3 Object Builder. This tool automates the generation of Resolution LODs and Geometry LODs, offering a user-friendly interface and customizable options to enhance your workflow.

## Overview

DayZ-LOD-Tools simplifies the process of generating LODs by providing an intuitive panel within Blender's 3D Viewport. It supports the creation of multiple resolution levels with adjustable decimation ratios, bounding box LODs, and the option to create empty objects with properties. The addon is optimized for Blender 4.5 and includes a refactored codebase for stability and performance.

## Features

- **Resolution LOD Generation**: Automatically create up to four resolution LODs with customizable decimation ratios using presets (Custom, Tris, Quads) or user-defined values.
- **Geometry LOD Options**: Generate a bounding box (Box) LOD or an empty object with properties (None) to meet various modeling needs.
- **Custom Properties**: Add and manage named properties for both Resolution and Geometry LODs to enhance object metadata.
- **Enhanced UI**: Features icons and tooltips for all controls, improving usability and visual clarity.
- **One-Click Processing**: Use the "Generate LODs" button to process all settings with a single action.

## Installation

1. **Download the Addon**  
   Clone or download this repository to your local machine.

2. **Install in Blender**  
   - Open Blender 4.5.
   - Go to `Edit > Preferences > Add-ons`.
   - Click `Install` and navigate to the downloaded `DayZ-LOD-Tools` folder.
   - Select the `__init__.py` file and click `Install Add-on`.
   - Enable the addon by checking the box next to "Arma 3 Object Builder Extensions".

3. **Verify Installation**  
   Switch to the 3D Viewport, open the sidebar (`N` key), and navigate to the `Object Builder` tab. The "Auto LODs Generator" panel should appear.

## Usage

### Accessing the Panel
- Open the 3D Viewport sidebar (`N` key).
- Select the `Object Builder` tab to find the "Auto LODs Generator" panel.

### Resolution LODs
- **Enable**: Check "Generate Resolution LODs" to activate.
- **Prefix**: Set a prefix for LOD object names (e.g., "resolution_lod_").
- **Start LOD**: Choose to start with "LOD 0" or "LOD 1".
- **Preset**: Select a decimation preset (Custom, Tris, Quads) or define custom ratios.
- **Named Properties**: Add custom properties to apply to all generated LODs.

### Geometry LOD
- **Enable**: Check "Generate Geometry LOD" to activate.
- **Name**: Specify the name for the Geometry LOD object.
- **Type**: Choose "Box" to create a bounding box or "None" for an empty object with properties.
- **Named Properties**: Add custom properties for the Geometry LOD.

### Generate LODs
- Click the "Generate LODs" button to process the selected options and create the LODs based on the active object.

## Requirements
- Blender 4.5 or later.

## Known Issues
- The addon does not account for modifiers affecting geometry (e.g., Subdivision Surface). Use applied geometry for accurate results.
- Report any bugs or feature requests on the GitHub Issues page.

## Contributing
- Fork the repository.
- Create a branch for your changes.
- Submit a pull request with your improvements.

## License
This addon is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the license terms.

## Contact
For support or inquiries, please open an issue on the GitHub repository or contact the authors directly.
