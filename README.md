# DayZ LOD Tools (Arma 3 Object Builder Extensions)

## Description
A Blender addon designed to automate and streamline the creation of LODs (Level of Detail) for DayZ and Arma 3 modding. It provides a comprehensive set of tools to generate Resolution, Geometry, Memory, Fire Geometry, and View Geometry LODs, ensuring they adhere to the correct naming conventions and property standards required by the game engine.

## Features

### Resolution LODs
- **Automated Generation**: Quickly create multiple visual LODs from your base mesh.
- **Decimation Presets**: Choose from built-in presets ('Tris', 'Quads') or define 'Custom' decimation ratios for each LOD level.
- **Smart Naming**: Automatically handles naming conventions (e.g., `Resolution 1`, `Resolution 2`).

### Geometry LOD
- **Collision Generation**: Create a simple bounding box or an empty container for your collision geometry.
- **Component Detection**: Integrates with Arma 3 Object Builder to automatically find and assign components.

### Memory LOD
- **Standard Points**: Automatically generates essential memory points:
    - `invview`: Inventory view point (correctly oriented to the object).
    - `boundingbox_min/max`: Bounding box corners.
    - `ce_radius` & `ce_center`: Central economy points.
- **Orientation Correct**: Memory points respect the object's rotation and scale.

### Fire Geometry LOD
- **Convex Hull Generation**: Creates accurate hit geometry using convex hulls.
- **Quality Control**: Adjustable quality slider to control the simplification (dissolve limit) of the generated hull.
- **Transform Safe**: Correctly handles object transformations during generation.

### View Geometry LOD
- **Occlusion Geometry**: Generates geometry for AI view occlusion.

### Named Properties
- **Dynamic Search**: Easily add and manage DayZ/Arma 3 specific properties.
- **Autocomplete**: Provides search and autocomplete for property names and values (requires Arma 3 Object Builder addon).

## Installation
1. Download the addon files.
2. Open Blender and navigate to **Edit > Preferences > Add-ons**.
3. Click **Install...** and select the addon file/folder.
4. Search for "Arma 3 Object Builder Extensions" and enable the checkbox.

## Usage
1. Locate the **Auto LODs Generator** panel in the **Object Builder** tab of the 3D View sidebar (N-panel).
2. Select the object you want to generate LODs for.
3. Enable the checkboxes for the LOD types you wish to generate.
4. Configure the settings for each LOD type (e.g., decimation ratios, quality, specific points).
5. Click the **Generate LODs** button.

## Dependencies
- **Arma 3 Object Builder**: This addon relies on the official/community Arma 3 Object Builder addon for property data definitions and component finding functionality. Ensure it is installed and enabled.

=======
Welcome to **DayZ LOD Tools** — an addon for Blender designed exclusively to work with **Arma 3 Object Builder**. 

This tool simplifies the process of creating models with various levels of detail (LODs) by providing a user-friendly interface and customizable parameters to enhance your workflow.

### Installation

To install the addon, follow these simple steps:

1.  **Download the addon**
    -   Go to the [Releases](https://github.com/yourusername/DayZ-LOD-Tools/releases) section on the GitHub page.
    -   Download the latest version of the addon as a `.zip` file.

2.  **Install the addon in Blender**
    -   Open Blender 4.5.
    -   Go to `Edit > Preferences > Add-ons`.
    -   Click the **"Install"** button.
    -   Select the downloaded `.zip` file and confirm the installation.
    -   Activate the addon by checking the box next to "Arma 3 Object Builder Extensions".

3.  **Verify the installation**
    -   Go to the 3D Viewport.
    -   Open the sidebar (press the `N` key).
    -   Navigate to the `Object Builder` tab. You should see the "Auto LODs Generator" panel.

### Requirements

-   **Blender 4.5 or newer**.
-   **Arma 3 Object Builder** is **mandatory** for the addon to work. The addon's functionality is not available without it.

### Key Features

-   Generate up to four levels of detail (LODs) with customizable simplification ratios.
-   Create geometric LODs (e.g., a bounding box) or empty objects with specified properties.
-   A convenient control panel in the 3D Viewport with icons and tooltips.

### Notes

-   Ensure you have [**Arma 3 Object Builder**](https://github.com/MrClock8163/Arma3ObjectBuilder) installed, as the addon is specifically designed to integrate with it.
-   Download the `.zip` file only from the official Releases section to avoid compatibility issues.

---

### Why this is important

-   I have added a note in the **"Requirements"** section stating that **Arma 3 Object Builder** is mandatory, so users will immediately understand this dependency.
-   The installation instructions now clearly describe the process of downloading the `.zip` from the Releases and using the "Install" button in Blender, as you specified.
