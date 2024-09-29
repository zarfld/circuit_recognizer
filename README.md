# ![CI Pipeline](https://github.com/zarfld/circuit_recognizer/actions/workflows/ci.yml/badge.svg)

# Circuit Recognizer Plugin for DIY Layout Creator

## Overview

The Circuit Recognizer Plugin enhances the functionality of the DIY Layout Creator by enabling users to automatically recognize and convert circuit diagrams from images or PDFs into editable layouts. This plugin uses the `circuit_recognizer` framework to interpret hand-drawn, digital, or scanned circuit diagrams and translate them into components that can be directly manipulated within the DIY Layout Creator interface.

## Key Features

- **Image and PDF Upload Interface**: Users can upload circuit diagrams in image formats (PNG, JPEG, BMP) or as PDFs. The plugin extracts relevant components from each page or image.
- **Automatic Component Recognition**: Detects components such as resistors, capacitors, transistors, diodes, and other standard electrical components in uploaded diagrams.
- **Schematic-to-Layout Conversion**: Converts recognized components and connections into editable objects that can be added to a new or existing DIY layout.
- **Visualization of Detected Components**: Automatically detected components are clearly displayed in full color, while unidentified or unrecognized components are marked in grey, allowing users to easily see which parts need manual attention.
- **Manual Marking and Correction Tools**: Users can manually select greyed-out components within the diagram and assign them as specific components (resistor, capacitor, diode, etc.). This allows the user to ensure every element is correctly identified.
- **Error Detection & Highlighting**: Lists potential errors, such as incomplete connections or unrecognizable components, which users can manually resolve.
- **Interactive Editing**: Users can click on any component in the diagram and modify its properties or placement before integrating it into the layout.
- **Integration with DIY Layout Creator**: Seamlessly integrates into the DIY Layout Creator interface, allowing users to drag-and-drop recognized and manually assigned components into the layout.
- **Component Library Mapping**: Automatically matches recognized components to the corresponding parts in the DIY Layout Creator’s component library.
- **Undo/Redo Functionality**: Supports undo and redo for edits made during the recognition and component assignment process.

## User Interface

- **Upload Section**: Allows users to upload circuit diagrams in both image formats and PDFs. Each page of a PDF is treated as a separate diagram.
- **Preview Window**: Displays the uploaded circuit diagram, highlighting:
  - **Detected Components**: Recognized components are shown in full color with labels.
  - **Undetected Components**: Unidentified components are highlighted in grey, prompting the user for manual input.
- **Error List**: Shows components or areas of the diagram where the recognition process needs manual correction, allowing users to quickly resolve issues.
- **Manual Component Assignment Tool**: Users can click on any greyed-out component and assign it a type (resistor, capacitor, diode, etc.) from a dropdown menu of recognized electrical components.
- **Component Palette**: Displays detected and manually assigned components. Users can drag these directly onto the DIY Layout Creator canvas for further layout design.
- **Settings Panel**: Configurable settings for recognition accuracy, error tolerance, and display preferences (e.g., color schemes for detected vs. undetected components).
- **Place on Layout**: A button to add the recognized circuit elements directly onto the current layout in DIY Layout Creator.

## How to Use

1. Upload an image or PDF of the circuit diagram using the plugin's upload interface.
2. Review the automatically recognized components in the Preview Window. Detected components will be in color, while undetected components will appear in grey.
3. Use the Manual Component Assignment Tool to select and assign greyed-out components to specific types (resistor, capacitor, etc.).
4. Drag recognized and manually assigned components from the Component Palette into your layout in DIY Layout Creator.
5. Use standard DIY Layout Creator tools to arrange, connect, and finalize the circuit layout.

## Manually Assigning Component Types

1. Click on any greyed-out component in the Preview Window.
2. Select the appropriate component type (resistor, capacitor, diode, etc.) from the dropdown menu.
3. The selected component will be updated and displayed in full color.

## Undo and Redo Functionality

1. To undo the last action, press `Ctrl + Z` or click the Undo button in the toolbar.
2. To redo the last undone action, press `Ctrl + Y` or click the Redo button in the toolbar.

## Integrating Recognized Components into DIY Layout Creator

1. After reviewing and manually assigning component types, drag the recognized components from the Component Palette.
2. Drop the components onto the DIY Layout Creator canvas.
3. Use the DIY Layout Creator tools to arrange and connect the components as needed.

## Requirements

- **DIY Layout Creator Version**: Requires version 3.2 or higher of DIY Layout Creator.
- **Supported Formats**: PNG, JPEG, BMP, PDF.
- **Browser Support**: Chrome, Firefox, Edge (latest versions).

## Future Enhancements

- **Improved OCR**: Enhance the detection of text annotations in the diagrams for better mapping to component labels.
- **Additional Component Support**: Add recognition for more specialized components like ICs, transformers, and user-defined components.
- **Live Editing**: Enable real-time recognition and manual editing within the DIY Layout Creator canvas.

## Installation

1. Download the Circuit Recognizer Plugin from the GitHub repository.
2. Place the plugin in the `plugins` directory of your DIY Layout Creator installation.
3. Restart DIY Layout Creator and access the plugin from the toolbar.

## License

This plugin is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## New Components Added

The recognition algorithm now supports additional components such as transistors, integrated circuits (ICs), and transformers. These components have been integrated into the `draw_result_boxes` function and the `output_file` function to ensure they are correctly recognized and labeled.

## Enhanced Image Preprocessing

The image preprocessing steps have been enhanced to improve the accuracy of component recognition. Advanced image processing techniques such as noise reduction, contrast enhancement, and edge detection have been implemented in the `handle_upload` function.

## Improved Machine Learning Model

The recognition algorithm now uses a more advanced machine learning model for component classification. The current model has been updated to incorporate Convolutional Neural Networks (CNNs) or other deep learning architectures, which have been trained on a larger dataset of labeled electrical components to achieve better recognition performance.

## Resistor Detection and Color Code Interpretation

The algorithm now includes a feature to detect resistors from a photo and interpret their color codes accurately. This feature supports 4-band, 5-band, and 6-band resistor color codes. The resistor's value, tolerance, and temperature coefficient (if applicable) are calculated and displayed.

### Key Objectives:

1. **Resistor Detection**:
   - Automatically detect the presence of resistors in a photo.
   - Identify different physical forms of resistors (e.g., axial lead, surface mount).
   - Locate and isolate the color bands from the detected resistor image.

2. **Color Code Recognition**:
   - Identify and interpret the color bands on the resistor to determine its resistance value.
   - Support different types of color codes based on the number of bands:
     - **4-band** resistors (most common, includes tolerance band).
     - **5-band** resistors (more precise, includes tolerance band).
     - **6-band** resistors (adds a temperature coefficient band).

3. **Handle Different Color Code Types**:
   - **4-band resistors**: First two bands represent digits, the third is the multiplier, and the fourth is the tolerance.
   - **5-band resistors**: First three bands represent digits, the fourth is the multiplier, and the fifth is the tolerance.
   - **6-band resistors**: Same as the 5-band resistor, but with an additional band for the temperature coefficient.

4. **Output the Resistor's Value**:
   - Calculate and display the resistance value based on the interpreted color code.
   - Show the tolerance and, in the case of 6-band resistors, the temperature coefficient.
   - Return the resistor's value in standard form (e.g., 1.2kΩ ±5%).

### Tasks:

1. **Resistor Detection from Image**:
   - Implement or integrate a computer vision algorithm to detect resistors in the image.
   - Use shape detection or edge detection to identify the cylindrical or rectangular shape of resistors.

2. **Isolate Color Bands**:
   - After detecting the resistor, focus on identifying the bands.
   - Use image segmentation techniques to isolate the color bands.
   - Ensure accurate identification despite lighting variations, shadows, and other noise.

3. **Color Code Interpretation**:
   - Map the detected color bands to their respective values.
   - Support 4-band, 5-band, and 6-band resistors.
   - Implement a method to calculate the resistance, tolerance, and temperature coefficient based on the bands.

4. **Handle Multiple Resistors in One Image**:
   - If multiple resistors are detected in a single image, provide results for each detected resistor.

5. **User Interface and Feedback**:
   - Display the detected resistor(s) with an overlay showing the identified color bands.
   - Show the calculated resistance value, tolerance, and temperature coefficient (if applicable).
   - Provide visual feedback on any errors or uncertainty in the detection.

### Considerations:

- **Lighting and Image Quality**: Ensure the algorithm can handle images with different lighting conditions, brightness, and contrast levels.
- **Orientation of Resistors**: The algorithm should be able to detect resistors regardless of their orientation (horizontal or vertical).
- **Common Resistor Color Codes**: Make sure to support the standard color code chart for resistors.

### Reference Resistor Color Code Chart:

| Color  | Digit | Multiplier       | Tolerance | Temperature Coefficient |
|--------|-------|------------------|-----------|-------------------------|
| Black  | 0     | 1 Ω              |           |                         |
| Brown  | 1     | 10 Ω             | ±1%       | 100 ppm/°C              |
| Red    | 2     | 100 Ω            | ±2%       | 50 ppm/°C               |
| Orange | 3     | 1,000 Ω          |           | 15 ppm/°C               |
| Yellow | 4     | 10,000 Ω         |           | 25 ppm/°C               |
| Green  | 5     | 100,000 Ω        | ±0.5%     |                         |
| Blue   | 6     | 1,000,000 Ω      | ±0.25%    |                         |
| Violet | 7     | 10,000,000 Ω     | ±0.1%     |                         |
| Grey   | 8     |                  | ±0.05%    |                         |
| White  | 9     |                  |           |                         |
| Gold   |       | 0.1 Ω            | ±5%       |                         |
| Silver |       | 0.01 Ω           | ±10%      |                         |

### Acceptance Criteria:

- The algorithm can successfully detect resistors from a photo and interpret their color codes.
- The feature supports 4-band, 5-band, and 6-band resistor color codes.
- The resistor's value (with tolerance and temperature coefficient if applicable) is calculated and displayed.
- The detection is robust against common image challenges (lighting, orientation, etc.).
- The feature provides a clear interface for users to interact with the detected resistors.
